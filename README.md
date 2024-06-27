# Report for Assignment 1

## Project chosen

Salt Project
URL: https://github.com/Pahal-7974/salt 

Number of lines of code and the tool used to count it: 57 kloc counted with lizard

Programming language: Python

## Coverage measurement

### Existing tool

Coverage.py was used as the coverage tool
The results were as follows:


https://github.com/Pahal-7974/salt/blob/master/images/sep%201.png

(https://github.com/Pahal-7974/salt/blob/master/images/sep%202.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%203.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%204.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%205.png)




### Your own coverage tool

### Varuni Sood

Function 1: unit>transport>test_ipc>def teardown(self)


URL: https://github.com/Pahal-7974/salt/commit/1b2942823a7228dde5195fa56a12335a14123bf5 
(https://github.com/Pahal-7974/salt/blob/master/images/v1.png)

Function 2: unit>transport>test_ipc>def test_multi_client_reading(self)


URL: https://github.com/Pahal-7974/salt/commit/e9a60bf5dba7660168c73c2c3842843786d3b872 
(https://github.com/Pahal-7974/salt/blob/master/images/v2.png)



### Pahal Agrawal

Function 1: unit>utils>test_botomod.py> def _has_required_boto()


URL: https://github.com/Pahal-7974/salt/commit/cc1929d4ae43fb75aa0614f1ddc2e494a4c85680
(https://github.com/Pahal-7974/salt/blob/master/images/p1.png)

Function 2: unit>states>test_module.py> def test_run_typed_return(self)


URL: https://github.com/Pahal-7974/salt/commit/9943b4425529fd381f42917251e116a88a78c870
(https://github.com/Pahal-7974/salt/blob/master/images/p2.png)



### Sakshi Sharma
URL: ​​https://github.com/Pahal-7974/salt/tree/sakshicherry4-patch-1
(https://github.com/Pahal-7974/salt/blob/master/images/s1.png)








return_something_after -> first function 
return_args_after ->  second function
(https://github.com/Pahal-7974/salt/blob/master/images/s2.png)




Function 1: unit>utils>test_timeout>return_something_after()
(https://github.com/Pahal-7974/salt/blob/master/images/s3.png)

Function 2: unit>utils>test_timeout>return_args_after()
(https://github.com/Pahal-7974/salt/blob/master/images/s4.png)



## Coverage improvement

### Individual tests



### Pahal Agrawal
Test 1: unit>utils>test_path.py


URL: https://github.com/Pahal-7974/salt/commit/676bfb5d48d5b3177be5af86e17fb8cbd4c27456
(https://github.com/Pahal-7974/salt/blob/master/images/p3.png)
(https://github.com/Pahal-7974/salt/blob/master/images/p4.png)


The coverage went from 78% to 79%. The file in question, test_path.py tests and checks for possible filepaths. However, not all edge cases are covered. I added a function to check for paths with empty strings and assert whether or not it works. Since the file is so big, The five branches I added (for loop iterations) increase the branch coverage by the seemingly low value of 1%.

Test 2: unit>utils>test_path.py


URL: https://github.com/Pahal-7974/salt/commit/676bfb5d48d5b3177be5af86e17fb8cbd4c27456
(https://github.com/Pahal-7974/salt/blob/master/images/p5.png)
(https://github.com/Pahal-7974/salt/blob/master/images/p6.png)

The coverage went from 79% to 80%. This is the same file as the one for the first test, hence the old coverage is the same as the new coverage for Test 1. I added a similar function to check if the application works with special characters in the paths. Both these are possible edge cases. The code that I added adds ten branches to the existing code, increasing the coverage by 1%.

### Varuni Sood
Test 1: unit>transport>test_ipc.py>test_empty_message(self)
URL: https://github.com/saltstack/salt/commit/8799995696914a1a02fb0ec17ca754e223cb7884 

Old coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v3.jpg)


New coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v4.png)



This function increases the coverage by three per cent. As the name suggests, its purpose is to verify how empty messages are handled. Since this is not appropriately being handled in the current code.

Test 2: unit>transport>test_ipc>test_large_message(self) and unit>transport>test_ipc>test_binary_data(self)


URL: https://github.com/saltstack/salt/commit/8799995696914a1a02fb0ec17ca754e223cb7884 

Old coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v5.png)


New coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v6.png)


The coverage increases by one per cent. The purpose is to enhance the system's ability to handle large messages and to process binary data correctly. The current code was not performing these actions effectively

Test 3: unit>transport>test_ipc>test_message_order(self)


URL: https://github.com/saltstack/salt/commit/8799995696914a1a02fb0ec17ca754e223cb7884 

Old coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v7.png)


New coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v8.png)


The coverage improvement is only one per cent, however, this checks a very important case, that is if messages are being received in the correct order. It ensures messages are being received in the same order as the one they are sent in and also can validate the system's ability to correctly handle asynchronous multiple message reads to a certain extent.

Test 4: unit>transport>test_ipc>test_error_handling_in_publisher functions, test_error_handling_in_subscriber


URL: https://github.com/saltstack/salt/commit/8799995696914a1a02fb0ec17ca754e223cb7884 

Old coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v9.png)


New coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/v10.png)


The coverage increases by two per cent. The function handles the response to the system when it attempts to publish messages on a closed channel and when it tries to read from a closed channel by raising exceptions.



### Sakshi Sharma

URL: https://github.com/Pahal-7974/salt/tree/sakshicherry4-patch-1

Old coverage results
(https://github.com/Pahal-7974/salt/blob/master/images/s5.png)


New coverage results

Test 1: def test_wait_for_negative_timeout(self)
(https://github.com/Pahal-7974/salt/blob/master/images/s6.png)

The coverage percentage increased from 60% to 66% with the help of this function. The function basically showcases that if a negative value is given to wait_for, the function returns False justifying its behavior while handling invalid input scenarios. This is an edge case which was not taken care of in the original code.


Test 2: def test_wait_for_function_returning_false(self)
The coverage increased from 66% to 68%. Basically handles a function that does not meet a certain requirement in a given/ specific amount of time. This is an edge case which was not taken care of in the original code.
(https://github.com/Pahal-7974/salt/blob/master/images/s7.png)


Test 3: def test_wait_for_timeout_equal_to_step(self)
The coverage went up from 68% to 71% because of this function. The wait_for correctly terminates the waiting process if the condition does not meet within the time frame in the first step itself.
(https://github.com/Pahal-7974/salt/blob/master/images/s8.png)


Test 4: def test_return_args_after_timeout(self):
Coverage increased from 71% to 80%. Method basically ensures that correct arguments are returned within a given timeout period.
(https://github.com/Pahal-7974/salt/blob/master/images/s9.png)



### Overall
Old Coverage(27%):

(https://github.com/Pahal-7974/salt/blob/master/images/sep%201.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%202.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%203.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%204.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep%205.png)






New Coverage (28%):

(https://github.com/Pahal-7974/salt/blob/master/images/sep6.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep7.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep8.png)

(https://github.com/Pahal-7974/salt/blob/master/images/sep9.png)


### Statement of individual contributions

### Sakshi:
tests-->unit->util->test_timeout.py
Created my own coverage measurement tool for 2 functions: return_something_after and return_args_after
Implemented 4 new functions to increase coverage:
def test_wait_for_negative_timeout(self)
def test_wait_for_function_returning_false(self)
def test_wait_for_timeout_equal_to_step(self)
def test_return_args_after_timeout(self)
  

### Varuni:
Coverage measurement tool for: tests>unit>transport>test_ipc.py>tearDown and tests>unit>transport>test_ipc.py>test_multi_client_reading
Enhanced the coverage by adding these: test_empty_message(self), test_large_message(self), test_binary_data(self), test_message_order(self), test_error_handling_in_publisher, test_error_handling_in_subscriber

### Pahal:
Code Instrumentation to create coverage measurement tool:
tests>unit>utils>test_botomod.py
tests>unit>states>test_module.py
Test Enhancement:
tests>unit>utils>test_path.py>test_join_with_empty_strings(self)
tests>unit>utils>test_path.py>test_join_with_special_characters(self)

Overall Coverage using existing tool:
Sakshi and Varuni (code did not work on Pahal’s system)
Contributions were still equal because of use of liveshare on VSC.



