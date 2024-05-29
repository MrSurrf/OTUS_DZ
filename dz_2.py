from abc import ABC, abstractmethod


class IPositionable(ABC):
    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def set_position(self, x,y):
        pass

class IMovable(ABC):
    # @abstractmethod
    # def get_position(self):
    #     pass
    #
    # @abstractmethod
    # def set_position(self, x,y):
    #     pass

    @abstractmethod
    def get_velosity(self):
        pass

class IRotatable(ABC):
    @abstractmethod
    def rotate_left(self):
        pass

    @abstractmethod
    def rotate_right(self):
        pass

    @abstractmethod
    def get_angle(self):
        pass


class SpaceShip(IMovable):
    def __init__(self):
        self.velocity = [1, 1]
        self.location = [0, 0]

    def GetLocation(self):
        return self.location

    def SetLocation(self, vector):
        self.location = vector
        print(self.location)

    def GetVelosity(self):
        return self.velocity


class SpaceShip1(IMovable):
    def __init__(self):
        self.velocity = [2, 2]
        self.location = [0, 0]

    def GetLocation(self):
        print(self.location)
        return self.location


    def SetLocation(self, vector):
        self.location = vector

    def GetVelosity(self):
        return self.velocity


class Vector:
    pass


class PositionableObject(IPositionable):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_position(self):
        return self._x, self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y


class MovableObject(PositionableObject, IMovable):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__(x, y)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

    # def get_position(self):
    #     pass
    #
    # def set_position(self, x, y):
    #     pass

    def get_velosity(self):
        return self._velocity_x, self._velocity_y

    def move(self):
        x, y = self.get_position()
        vx, vy = self.get_velocity()
        self.set_position(x + vx, y + vy)


class RotatableObject(PositionableObject, IRotatable):
    def __init__(self, x, y, angle=0):
        super().__init__(x, y)
        self._angle = angle

    def rotate_left(self):
        self._angle = (self._angle - 90) % 360

    def rotate_right(self):
        self._angle = (self._angle + 90) % 360

    def get_angle(self):
        return self._angle


# class Move:
#     def move(self, movable: IMovable):
#         loc = movable.GetLocation()
#         vel = movable.GetVelosity()
#         loc[0] += vel[0]
#         loc[1] += vel[1]
#         movable.SetLocation(loc)
#         # Сложить текущую локацию и скорость
#
#
# class Rotate:
#     def rotate(self, movable: IMovable):
#         pass
#
#
# def run():
#     s = SpaceShip()
#     s1 = SpaceShip1()
#     m = Move()
#
#     m.move(s1)
#     s1.GetLocation()
#     m.move(s1)
#     s1.GetLocation()
#     m.move(s1)
#     s1.GetLocation()


# run()
