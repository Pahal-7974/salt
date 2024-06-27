import logging
import time
import pytest
from salt.utils.timeout import wait_for
from tests.support.unit import TestCase

log = logging.getLogger(__name__)


branch_coverage = {
    "return_something_after": {"branch_1_hit": False, "branch_2_hit": False},
    "return_args_after": {"branch_3_hit": False, "branch_4_hit": False},
}


def log_coverage():
    with open('timeout_cov.txt', 'w') as f:
        branches_hit = 0
        total_branches = 0
        for func, branches in branch_coverage.items():
            for branch, hit in branches.items():
                branch_num = branch.split('_')[1]
                hit_miss = "Hit" if hit else "Missed"
                f.write(f"Branch {branch_num}: {hit_miss}\n")
                if hit:
                    branches_hit += 1
                total_branches += 1
        f.write(f"\nBranches Hit: {branches_hit}/{total_branches} ({branches_hit / total_branches * 100:.1f}%)\n")


def return_something_after(seconds, something=True):
    start = time.time()
    end = start + seconds
    log.debug("Will return %s at %s", something, end)

    def actual():
        t = time.time()
        condition = t >= end
        log.debug("Return something at %s ? %s", t, condition)
        if condition:
            branch_coverage["return_something_after"]["branch_1_hit"] = True
            return something
        else:
            branch_coverage["return_something_after"]["branch_2_hit"] = True
            return False

    return actual


def return_args_after(seconds):
    start = time.time()
    end = start + seconds

    def actual(*args):
        if time.time() >= end:
            branch_coverage["return_args_after"]["branch_3_hit"] = True
            return args
        else:
            branch_coverage["return_args_after"]["branch_4_hit"] = True
            return False

    return actual


def return_kwargs_after(seconds):
    start = time.time()
    end = start + seconds

    def actual(**kwargs):
        if time.time() >= end:
            return kwargs
        else:
            return False

    return actual


class WaitForTests(TestCase):
    def setUp(self):
        self.true_after_1s = return_something_after(1)
        self.self_after_1s = return_something_after(1, something=self)

    def tearDown(self):
        log_coverage()
        del self.true_after_1s
        del self.self_after_1s

    @pytest.mark.slow_test
    def test_wait_for_true(self):
        ret = wait_for(self.true_after_1s, timeout=2, step=0.5)
        self.assertTrue(ret)

    @pytest.mark.slow_test
    def test_wait_for_self(self):
        ret = wait_for(self.self_after_1s, timeout=2, step=0.5)
        self.assertEqual(ret, self)

    def test_wait_for_too_long(self):
        ret = wait_for(self.true_after_1s, timeout=0.5, step=0.1, default=False)
        self.assertFalse(ret)

    @pytest.mark.slow_test
    @pytest.mark.skip_initial_gh_actions_failure
    def test_wait_for_with_big_step(self):
        ret = wait_for(self.true_after_1s, timeout=1.5, step=2)
        self.assertTrue(ret)

    @pytest.mark.slow_test
    def test_wait_for_custom_args(self):
        args_after_1s = return_args_after(1)
        args = ("one", "two")
        ret = wait_for(args_after_1s, timeout=2, step=0.5, func_args=args)
        self.assertEqual(ret, args)

    @pytest.mark.slow_test
    def test_wait_for_custom_kwargs(self):
        kwargs_after_1s = return_kwargs_after(1)
        kwargs = {"one": 1, "two": 2}
        ret = wait_for(kwargs_after_1s, timeout=2, step=0.5, func_kwargs=kwargs)
        self.assertEqual(ret, kwargs)

    def test_return_false(self):
        ret = self.true_after_1s()
        self.assertFalse(ret)
