"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple, Optional


class Facing(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid():
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}

    @property
    def current_pos(self) -> Tuple[int, int]:
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:
        # Question 1: current_pos setter 实现
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError("Position must be a tuple of length 2")

        # 强制转换为 int 并限制在网格范围内
        x = max(0, min(int(value[0]), self.width))
        y = max(0, min(int(value[1]), self.height))

        self._current_pos = (x, y)

    def move_forward(self) -> Tuple[int, int]:
        # Question 2: 向前移动
        x, y = self.current_pos

        if self.current_direction == Facing.RIGHT:
            new_pos = (x + 1, y)
        elif self.current_direction == Facing.UP:
            new_pos = (x, y + 1)
        elif self.current_direction == Facing.LEFT:
            new_pos = (x - 1, y)
        elif self.current_direction == Facing.DOWN:
            new_pos = (x, y - 1)
        else:
            new_pos = (x, y)

        # 使用 setter 来设置新位置（会自动限制范围）
        self.current_pos = new_pos
        return self.current_pos

    def turn_left(self) -> Facing:
        # Question 3a: 逆时针转向
        current_value = self.current_direction.value
        new_value = (current_value + 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def turn_right(self) -> Facing:
        # Question 3b: 顺时针转向
        current_value = self.current_direction.value
        new_value = (current_value - 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def find_enemy(self) -> bool:
        # Question 4: 检查是否找到敌人
        return self.current_pos == self.enemy_pos

    def record_position(self, step: int) -> None:
        # Question 5a: 记录位置历史
        self.position_history[step] = self.current_pos

    def get_position_at_step(self, step: int) -> Optional[tuple]:
        # Question 5b: 获取指定步数的位置
        return self.position_history.get(step, None)


class AdvancedGrid(Grid):
    """
    AdvancedGrid 类，继承自 Grid 类
    新增功能：
    1. 追踪移动步数
    2. 计算到敌人的曼哈顿距离
    """

    def __init__(self, width: int, height: int, enemy_pos: tuple):
        # 调用父类初始化
        super().__init__(width, height, enemy_pos)
        # 新增属性：移动步数计数器
        self.steps: int = 0

    def move_forward(self) -> Tuple[int, int]:
        """
        重写 move_forward 方法
        调用父类的移动方法，然后增加步数计数
        """
        # 调用父类的移动方法
        new_pos = super().move_forward()

        # 移动步数加 1
        self.steps += 1

        # 记录当前位置到历史（使用当前步数）
        self.record_position(self.steps)

        return new_pos

    def distance_to_enemy(self) -> int:
        """
        计算当前位置到敌人位置的曼哈顿距离
        曼哈顿距离 = |x1 - x2| + |y1 - y2|
        """
        current_x, current_y = self.current_pos
        enemy_x, enemy_y = self.enemy_pos

        distance = abs(current_x - enemy_x) + abs(current_y - enemy_y)
        return distance
