from time import sleep
from enum import IntEnum
import termcolor2
from emoji import emojize

import os

"""
y = افقی
x = عمودی
"""


class CellType(IntEnum):
    PATH = 1
    FREE = 2


my_map = None


class Direction(IntEnum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Cell:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._contents = []

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def get_content(self):
        return self._contents

    # @property
    # def typ(self):
    #     return self._typ
    #
    # @typ.setter
    # def typ(self, type_item):
    #     self._typ = type_item

    def add_content(self, item):
        self._contents.append(item)

    def remove_content(self, item):
        self._contents.remove(item)

    def __str__(self):
        return " ".join([str(content) for content in self._contents]).center(11)


class Map:
    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._board = []
        self._bullets = []
        self._zombies = []
        self._tower = []

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def board(self):
        return self._board

    # def initialize(self):
    #     for row in range(self._height):
    #         rows = []
    #         for cul in range(self._width):
    #             cell = Cell(x=cul, y=row, typ=CellType.FREE.value)
    #             rows.append(cell)
    #
    #         self._board.append(rows)

    # def init_path(self):
    #     for row in range(self._height):
    #         cell: Cell = self._board[row][-1]
    #         cell.typ = CellType.PATH.value
    #         self._path.append(cell)
    #
    #     for cul in range(self._width - 1, -1, -1):
    #         cell: Cell = self._board[self._height - 1][cul]
    #         cell.typ = CellType.PATH.value
    #         self._path.append(cell)

    def initialize(self):
        for y in range(self._height):
            row = []
            for x in range(self._width):
                cell = Cell(x=x, y=y)
                row.append(cell)

            self._board.append(row)

    def print_board(self):
        roof = "/" * (self._width * (self._width + 2) + 1)
        # print(roof)
        for y in range(self._height):
            print("" + "".join([str(cell) for cell in self._board[y]]) + "")
            print(roof)
        print()

    @property
    def bullets(self):
        return self._bullets

    def add_bullet(self, bullet):
        self._bullets.append(bullet)

    def remove_bullet(self, bullet):
        self._bullets.remove(bullet)

    @property
    def towers(self):
        return self._tower

    def add_tower(self, tower):
        self._tower.append(tower)

    def remove_flower(self, tower):
        self._tower.remove(tower)

    @property
    def zombies(self):
        return self._zombies

    def add_zombie(self, zombie):
        self._zombies.append(zombie)

    def remove_zombie(self, zombie):
        self._zombies.remove(zombie)


class Obj:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def add_to_map(self):
        global my_map

        if isinstance(self, Bullet):
            my_map.add_bullet(self)

        elif isinstance(self, Tower):
            my_map.add_tower(self)

        elif isinstance(self, Zombie):
            my_map.add_zombie(self)

        my_map.board[self._x][self._y].add_content(self)

    def remove_from_map(self):
        global my_map
        if isinstance(self, Bullet):
            my_map.remove_bullet(self)

        my_map.board[self._x][self._y].remove_content(self)


class Movable(Obj):

    def movement(self, direction: int):
        global my_map
        prev_x = self._x
        prev_y = self._y

        if direction == Direction.RIGHT.value:
            new_x = self._x
            new_y = self._y + 1

        elif direction == Direction.LEFT.value:
            new_x = self._x
            new_y = self._y - 1

        elif direction == Direction.UP.value:
            new_x = self._x - 1
            new_y = self._y

        elif direction == Direction.DOWN.value:
            new_x = self._x + 1
            new_y = self._y
        else:
            print(f"Invalid direction. {direction}")
            return
        try:
            if new_x < 0 or new_x >= my_map.height or new_y < 0 or new_y >= my_map.width:
                my_map.board[prev_x][prev_y].remove_content(self)
                my_map.remove_bullet(self)
            else:
                my_map.board[prev_x][prev_y].remove_content(self)
                my_map.board[new_x][new_y].add_content(self)
                self._x = new_x
                self._y = new_y
        except:
            print(termcolor2.colored("GAME OVER", color="cyan", ), "🏁")


class Bullet(Movable):

    def __init__(self, x, y):
        super(Bullet, self).__init__(x, y)

    @property
    def damage(self):
        raise NotImplemented

    def move(self):
        raise NotImplemented

    def remove(self):
        raise NotImplemented

    def __str__(self):
        raise NotImplemented


class Strong_Bullet(Bullet):

    def __init__(self, x, y):
        # self._speed = speed
        self._damage = 50
        super(Strong_Bullet, self).__init__(x, y)

    @property
    def damage(self):
        return self._damage

    def move(self):
        super(Strong_Bullet, self).movement(Direction.RIGHT.value)

    def remove(self):
        my_map.board[self.x][self.y].remove_content(self)
        my_map.remove_bullet(self)

    def __str__(self):
        return "🔥"


class Weak_Bullet(Bullet):

    def __init__(self, x, y):
        # self._speed = speed
        self._damage = 25
        super(Weak_Bullet, self).__init__(x, y)

    @property
    def damage(self):
        return self._damage

    def move(self):
        super(Weak_Bullet, self).movement(Direction.RIGHT.value)

    def remove(self):
        my_map.board[self.x][self.y].remove_content(self)
        my_map.remove_bullet(self)

    def __str__(self):
        return "❄"


class Tower(Obj):
    def __init__(self, x, y):
        self._damage = 50
        super(Tower, self).__init__(x, y)

    @property
    def damage(self):
        return self._damage

    def shoot(self):
        raise NotImplemented


class Strong_Tower(Tower):
    def __init__(self, x, y):
        self._damage = 75
        self._timetodeath = 30
        super(Strong_Tower, self).__init__(x, y)

    def __str__(self):
        return emojize(":castle:")

    def shoot(self):
        bullet = Strong_Bullet(self._x + 1, self._y)
        bullet.add_to_map()


class Weaktower(Tower):
    def __init__(self, x, y):
        self._damage = 50
        self._timetodeath = 20
        super(Weaktower, self).__init__(x, y)

    def __str__(self):
        return "🎪"

    def shoot(self):
        bullet = Weak_Bullet(self._x + 1, self._y)
        bullet.add_to_map()


class Zombie(Movable):

    def __init__(self, x, y):
        self._speed = 2
        super(Zombie, self).__init__(x, y)

    @property
    def speed(self):
        return self._speed

    def move(self):
        super(Zombie, self).movement(Direction.LEFT.value)

    def remove(self):
        raise NotImplemented

    def damage(self, bullet):
        raise NotImplemented


class Big_Zombie(Zombie):

    def __init__(self, x, y):
        self._hp = 50
        super(Big_Zombie, self).__init__(x, y)

    def __str__(self):
        return "🧛"

    def remove(self):
        my_map.board[self.x][self.y].remove_content(self)
        my_map.remove_zombie(self)

    def damage(self, bullet):
        self._hp -= bullet.damage
        bullet.remove()

        if self._hp <= 0:
            self.remove()


class Small_Zombie(Zombie):

    def __init__(self, x, y):
        self._hp = 100
        super(Small_Zombie, self).__init__(x, y)

    def __str__(self):
        return "🧟"

    def remove(self):
        my_map.board[self.x][self.y].remove_content(self)
        my_map.remove_zombie(self)

    def damage(self, bullet):
        self._hp -= bullet.damage
        bullet.remove()

        if self._hp <= 0:
            self.remove()


class Engine:

    def __init__(self):
        pass

    def run(self):
        global my_map
        my_map = Map(2, 14)
        my_map.initialize()

        weak_tower = Weaktower(0, 6)
        weak_tower.add_to_map()
        weak_tower.shoot()

        weak_tower1 = Weaktower(0, 2)
        weak_tower1.add_to_map()
        weak_tower1.shoot()

        strong_tower = Strong_Tower(0, 1)
        strong_tower.add_to_map()
        strong_tower.shoot()

        strong_tower1 = Strong_Tower(0, 3)
        strong_tower1.add_to_map()
        strong_tower1.shoot()

        small_zombie = Small_Zombie(1, 13)
        small_zombie.add_to_map()

        big_zombie = Big_Zombie(1, 12)
        big_zombie.add_to_map()

        small_zombie1 = Small_Zombie(1, 11)
        small_zombie1.add_to_map()

        big_zombie1 = Big_Zombie(1, 10)
        big_zombie1.add_to_map()

        counter = 1
        while True:
            print("\n\n\n\n")
            print(f"time : {counter}s")
            my_map.print_board()
            sleep(1)

            # move bullets

            for bullet in my_map.bullets:
                bullet.move()

            for bullet in my_map.bullets:
                for zombie in my_map.zombies:
                    if bullet.x == zombie.x and bullet.y == zombie.y:
                        zombie.damage(bullet)

            # move zombies
            for zombie in my_map.zombies:
                if counter % zombie.speed == 0:
                    zombie.move()

            if counter == 24:
                break

            counter += 1


if __name__ == "__main__":
    engine = Engine()
    engine.run()
