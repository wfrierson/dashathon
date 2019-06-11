"""Collection of function to test the unit test cases"""
from dataframe import converttime_checker
from dataframe import pipe_reader_checker


def test_converttime():
    """Testing for converting HH:MM:SS to seconds"""
    assert converttime_checker('23:59:59')


def test_pipe_reader():
    """Testing for (22824, 20) shape in the dataset"""
    assert pipe_reader_checker('/ihme/homes/edwin100/notebooks/515/'
                               'boston_marathon_dashboard/data/'
                               'chicago_marathon_2017_M.csv')

# For running the unit tests, execute below two functions
test_converttime()
test_pipe_reader()
