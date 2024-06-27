"""
    :codeauthor: Mike Place <mp@saltstack.com>
"""

import errno
import logging
import os
import threading

import pytest
import tornado.gen
import tornado.ioloop
import tornado.testing
from tornado.iostream import StreamClosedError

import salt.config
import salt.exceptions
import salt.transport.ipc
import salt.utils.platform
from tests.support.runtests import RUNTIME_VARS

pytestmark = [
    pytest.mark.skip_on_darwin,
    pytest.mark.skip_on_freebsd,
    pytest.mark.skip_on_windows,
]

log = logging.getLogger(__name__)

coverage = {i: False for i in range(1, 9)}

def branch_hit(branch_id):
    coverage[branch_id] = True

@pytest.mark.skip_on_windows(reason="Windows does not support Posix IPC")
class IPCMessagePubSubCase(tornado.testing.AsyncTestCase):
    """
    Test all of the clear msg stuff
    """
    coverage_file_path = os.path.join(os.getcwd(), "test_ipc_coverage.txt")
    total_branches = len(coverage)
    branches_hit = sum(1 for hit in coverage.values() if hit)

    with open(coverage_file_path, "w") as f:
        for branch_id in range(1, total_branches + 1):
            hit_status = 'Hit' if coverage[branch_id] else 'Missed'
            f.write(f"Branch {branch_id}: {hit_status}\n")
        percentage_hit = (branches_hit / total_branches) * 100
        f.write(f"\nBranches Hit: {branches_hit}/{total_branches} ({percentage_hit:}%)\n")

    def setUp(self):
        super().setUp()
        self.opts = {"ipc_write_buffer": 0}
        if not os.path.exists(RUNTIME_VARS.TMP):
            os.mkdir(RUNTIME_VARS.TMP)
        self.socket_path = os.path.join(RUNTIME_VARS.TMP, "ipc_test.ipc")
        self.pub_channel = self._get_pub_channel()
        self.sub_channel = self._get_sub_channel()

    def _get_pub_channel(self):
        pub_channel = salt.transport.ipc.IPCMessagePublisher(
            self.opts,
            self.socket_path,
        )
        pub_channel.start()
        return pub_channel

    def _get_sub_channel(self):
        sub_channel = salt.transport.ipc.IPCMessageSubscriber(
            socket_path=self.socket_path,
            io_loop=self.io_loop,
        )
        sub_channel.connect(callback=self.stop)
        self.wait()
        return sub_channel

    def tearDown(self):
        super().tearDown()
        try:
            branch_hit(1)
            self.pub_channel.close()
        except RuntimeError as exc:
            branch_hit(2)
            pass
        except OSError as exc:
            branch_hit(3)
            if exc.errno != errno.EBADF:
                # If its not a bad file descriptor error, raise
                raise
        try:
            branch_hit(4)
            self.sub_channel.close()
        except RuntimeError as exc:
            branch_hit(5)
            pass
        except OSError as exc:
            branch_hit(6)
            if exc.errno != errno.EBADF:
                # If its not a bad file descriptor error, raise
                raise
        os.unlink(self.socket_path)
        del self.pub_channel
        del self.sub_channel

    def test_multi_client_reading(self):
        # To be completely fair let's create 2 clients.
        client1 = self.sub_channel
        client2 = self._get_sub_channel()
        call_cnt = []

        # Create a watchdog to be safe from hanging in sync loops (what old code did)
        evt = threading.Event()

        def close_server():
            if evt.wait(1):
                return
            client2.close()
            self.stop()

        watchdog = threading.Thread(target=close_server)
        watchdog.start()

        # Runs in ioloop thread so we're safe from race conditions here
        def handler(raw):
            call_cnt.append(raw)
            if len(call_cnt) >= 2:
                branch_hit(7)
                evt.set()
                self.stop()
            else: branch_hit(8)

        # Now let both waiting data at once
        client1.read_async(handler)
        client2.read_async(handler)
        self.pub_channel.publish("TEST")
        self.wait()
        self.assertEqual(len(call_cnt), 2)
        self.assertEqual(call_cnt[0], "TEST")
        self.assertEqual(call_cnt[1], "TEST")
    

    def test_sync_reading(self):
        # To be completely fair let's create 2 clients.
        client1 = self.sub_channel
        client2 = self._get_sub_channel()
        call_cnt = []

        # Now let both waiting data at once
        self.pub_channel.publish("TEST")
        ret1 = client1.read_sync()
        ret2 = client2.read_sync()
        self.assertEqual(ret1, "TEST")
        self.assertEqual(ret2, "TEST")

    @tornado.testing.gen_test
    def test_async_reading_streamclosederror(self):
        client1 = self.sub_channel
        call_cnt = []

        # Create a watchdog to be safe from hanging in sync loops (what old code did)
        evt = threading.Event()

        def close_server():
            if evt.wait(0.001):
                return
            client1.close()
            self.stop()

        watchdog = threading.Thread(target=close_server)
        watchdog.start()

        # Runs in ioloop thread so we're safe from race conditions here
        def handler(raw):
            pass

        try:
            ret1 = yield client1.read_async(handler)
            self.wait()
        except StreamClosedError as ex:
            assert False, "StreamClosedError was raised inside the Future"

#additional tests
    def test_message_order(self):
        client1 = self.sub_channel
        messages = ["message1", "message2", "message3"]
        received_messages = []

        def handler(raw):
            received_messages.append(raw)
            if len(received_messages) == len(messages):
                self.stop()

        for msg in messages:
            self.pub_channel.publish(msg)

        client1.read_async(handler)
        self.wait()
        self.assertEqual(received_messages, messages)

    def test_empty_message(self):
        client1 = self.sub_channel

        def handler(raw):
            self.assertEqual(raw, "")
            self.stop()

        self.pub_channel.publish("")
        client1.read_async(handler)
        self.wait()

    def test_large_message(self):
        client1 = self.sub_channel
        large_message = "A" * 1024 * 1024

        def handler(raw):
            self.assertEqual(raw, large_message)
            self.stop()

        self.pub_channel.publish(large_message)
        client1.read_async(handler)
        self.wait()

    def test_binary_data(self):
        client1 = self.sub_channel
        binary_data = b"\x00\xFF\xFE\xFD"

        def handler(raw):
            self.assertEqual(raw, binary_data)
            self.stop()

        self.pub_channel.publish(binary_data)
        client1.read_async(handler)
        self.wait()

    def test_error_handling_in_publisher(self):
        pub_channel = self.pub_channel
        pub_channel.close()

        with self.assertRaises(salt.exceptions.SaltMasterError):
            pub_channel.publish("TEST")

    def test_error_handling_in_subscriber(self):
        client1 = self.sub_channel
        client1.close()

        with self.assertRaises(StreamClosedError):
            client1.read_sync()
