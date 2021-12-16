import importlib
import inspect
import traceback

SUCCESS_MSG = "Success"

def evaluate_tests(module, tests):
    record = dict()

    for name, test in tests.items():
        try:
            test(module)
            record[name] = SUCCESS_MSG
        except:
            record[name] = traceback.format_exc()
    return record

def write_to_record(record_ndsi, record_predict, folder_name):
    tests = list(record_ndsi.items()) + list(record_predict.items())
    passed_tests = list(filter(lambda test:test[1] == SUCCESS_MSG, tests))

    with open(f"{folder_name}/record", "w") as record_file:
        record_file.write(f"Passed tests: {len(passed_tests)}/{len(tests)}\n\n")
        record_file.write(f"{'NDSI':=^30}\n")
        record_file.write("\n\n".join([f"{test}\n{message}"
                                       for test, message
                                       in record_ndsi.items()]))
        record_file.write("\n")
        record_file.write(f"{'Predict':=^31}\n")
        record_file.write("\n\n".join([f"{test}\n{message}"
                                       for test, message
                                       in record_predict.items()]))
def tuples2dict(tuples):
    return {key:value for key, value in tuples}

def istest(func):
    if not inspect.isfunction(func):
        return False
    
    try:
        params = inspect.signature(func).parameters
        if params['module'].name == 'module' and len(params) == 1:
            return True
    except:
        return False

def do_main(folder_name):
    ndsi_module = importlib.import_module(f"{folder_name}.ndsi")
    predict_module = importlib.import_module(f"{folder_name}.predict")

    ndsi_tests_module = importlib.import_module("tests.ndsi")
    predict_tests_module = importlib.import_module("tests.predict")

    ndsi_tests = inspect.getmembers(ndsi_tests_module, istest)
    predict_tests = inspect.getmembers(predict_tests_module, istest)
    
    record_ndsi = evaluate_tests(ndsi_module, tuples2dict(ndsi_tests))
    record_predict = evaluate_tests(predict_module, tuples2dict(predict_tests))
    
    write_to_record(record_ndsi, record_predict, folder_name)

def translate_file(filename):
    file_to_translate = open(filename, "r")
    lines = [(line if "__name__" not in line else "def main():\n")
             for line in file_to_translate.readlines()]
    file_to_translate.close()
    with open(filename, "w") as translated_file:
        translated_file.writelines(lines)

def preprocess_folder(folder_name):
    translate_file(f"{folder_name}/ndsi.py")
    translate_file(f"{folder_name}/predict.py")

def main():
    # change these to your folders
    folders = []
    
    for folder in folders:
        # uncomment this to do the preprocessing
        # i.e., if you would also like to test the main function
        # I'd advise against it because it's cumbersom to clean up
        preprocess_folder(folder)
        print()
        print(f"{'='*30}\nTesting {folder}...")
        do_main(folder)

if __name__ == "__main__":
    main()
