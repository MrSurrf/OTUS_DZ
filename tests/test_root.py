import sys
import unittest
from unittest.mock import Mock, create_autospec
sys.path.append('../OTUS_DZ')
from quadratic_equation import quadratic_equation

from dz_2 import *


def test_quadratic():
    assert len(quadratic_equation(1.0, 0, 1.0, 0.0001)) == 0


def test_multi_two():
    assert len(quadratic_equation(1.0, 0, -1.0, 0.0001)) == 2


def test_multi_one():
    assert len(quadratic_equation(1, 2.00001, 1, 0.0001)) == 1


# def test_equal_zero():
#     assert quadratic_equation(0.001, 1, 1, 0.0001) == -1


def test_type():
    try:
        quadratic_equation('str', True, None, 7)
        assert False
    except:
        assert True



class TestMovableObject(unittest.TestCase):
    def test_move(self):
        mock_m = create_autospec(IMovable, instance=True)
        mock_m.get_position.return_value = (12, 5)
        mock_m.get_velocity.return_value = (-7, 3)
        move_command = MoveCommand(mock_m)
        move_command.execute()
        mock_m.set_position.assert_called_with((5, 8))
        # obj = MovableObject(12, 5, -7, 3)
        # obj.move()
        # self.assertEqual(obj.get_position(), (5, 8))

    def test_move_invalid_position(self):

        mock_m = create_autospec(IMovable, instance=True)

        mock_m.get_position.return_value = None

        move_command = MoveCommand(mock_m)

        with self.assertRaises(TypeError):
            move_command.execute()

        # with self.assertRaises(TypeError):
        #     obj = MovableObject("invalid", 5, -7, 3)
        #     obj.move()

    def test_move_invalid_velocity(self):

        mock_m = create_autospec(IMovable, instance=True)

        mock_m.get_velocity.return_value = None

        move_command = MoveCommand(mock_m)

        with self.assertRaises(TypeError):
            move_command.execute()


        # with self.assertRaises(TypeError):
        #     obj = MovableObject(12, 5, "invalid", 3)
        #     obj.move()

    def test_move_invalid_to_set_position(self):

        mock_m = create_autospec(IMovable, instance=True)

        mock_m.set_position.side_effect = AttributeError

        move_command = MoveCommand(mock_m)

        with self.assertRaises(AttributeError):
            move_command.execute()

        # class NonPositionable:
        #     def get_position(self):
        #         return 0, 0
        #
        # obj = MovableObject(12, 5, -7, 3)
        # obj.set_position = NonPositionable().get_position
        # with self.assertRaises(TypeError):
        #     obj.move()

class TestRotatableObject(unittest.TestCase):

    def test_rotate_left(self):

        mock_r = create_autospec(IRotatable)

        rotate_command = RotateCommand(mock_r, 'left')

        rotate_command.execute()

        mock_r.rotate_left.assert_called_once()

    def test_rotate_right(self):

        mock_r = create_autospec(IRotatable)

        rotate_command = RotateCommand(mock_r, 'right')

        rotate_command.execute()

        mock_r.rotate_right.assert_called_once()

    # def test_rotate_left(self):
    #     obj = RotatableObject(0, 0)
    #     obj.rotate_left()
    #     self.assertEqual(obj.get_angle(), 270)
    #
    # def test_rotate_right(self):
    #     obj = RotatableObject(0, 0)
    #     obj.rotate_right()
    #     self.assertEqual(obj.get_angle(), 90)

if __name__ == '__main__':
    unittest.main()






