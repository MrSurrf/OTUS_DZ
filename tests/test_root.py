import sys

sys.path.append('../OTUS_DZ')
from quadratic_equation import quadratic_equation


def test_quadratic():
    assert len(quadratic_equation(1.0, 0, 1.0, 0.0001)) == 0


def test_multi_two():
    assert len(quadratic_equation(1.0, 0, -1.0, 0.0001)) == 2


def test_multi_one():
    assert len(quadratic_equation(1, 2.00001, 1, 0.0001)) == 1


def test_equal_zero():

    assert quadratic_equation(0.001,1,1,0.0001) == -1

def test_type():
    try:
        quadratic_equation('str', True, None, 7)
        assert False
    except:
        assert True
