import sys

sys.path.append('../OTUS_DZ')
from quadratic_equation import quadratic_equation

from dz_2 import *


def test_quadratic():
    assert len(quadratic_equation(1.0, 0, 1.0, 0.0001)) == 0


def test_multi_two():
    assert len(quadratic_equation(1.0, 0, -1.0, 0.0001)) == 2


def test_multi_one():
    assert len(quadratic_equation(1, 2.00001, 1, 0.0001)) == 1


def test_equal_zero():
    assert quadratic_equation(0.001, 1, 1, 0.0001) == -1


def test_type():
    try:
        quadratic_equation('str', True, None, 7)
        assert False
    except:
        assert True

def test_move(self):
    obj = MovableObject(12, 5, -7, 3)
    obj.move()
    self.assertEqual(obj.get_position(), (5, 8))
def test_move_invalid_position(self):
    with self.assertRaises(TypeError):
        obj = MovableObject("invalid", 5, -7, 3)
        obj.move()

def test_move_invalid_velocity(self):
    with self.assertRaises(TypeError):
         obj = MovableObject(12, 5, "invalid", 3)
         obj.move()

def test_move_unable_to_set_position(self):
    class NonPositionable:
        def get_position(self):
            return 0, 0

    obj = MovableObject(12, 5, -7, 3)
    obj.set_position = NonPositionable().get_position
    with self.assertRaises(TypeError):
        obj.move()

def test_rotate_left(self):
    obj = RotatableObject(0, 0)
    obj.rotate_left()
    self.assertEqual(obj.get_angle(), 270)

def test_rotate_right(self):
    obj = RotatableObject(0, 0)
    obj.rotate_right()
    self.assertEqual(obj.get_angle(), 90)






