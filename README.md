Small test suite for TP3 DDP1 Gasal 2021/2022


Write the respective module's tests in `tests/ndsi.py` and `tests/predict.py`.
**Every** test must have `module` as its first argument, and this will be the interface to the actual module of the student's submission. See current files for reference.



**To test the main block**: uncomment line 83 in `test_TP3.py` and remove the `PLACEHOLDER` variables in the function signature for `test_main` in `tests/ndsi.py` and `tests/predict.py`.



**Important**: because the grading is fault-tolerant, **print** your relevant results before assertions to evaluate whether a test actually failed or not. In the current tests there are already printed results, but your needs may vary. Change accordingly.



Run by evaluating the file `test_TP3.py`. `sampling.py` is to take a small sample from the whole dataset to speed-up testing.


It's advised to pipe STDOUT when running the program to a separate record file as a means of documentation, but you can also not do that and just read off of the terminal.
