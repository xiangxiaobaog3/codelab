class BaseEntity(object):

    """"""

    def __init__(self):
        self.id = None

    def set_id(self, id_):
        self.id = id_


class MovingEntity(BaseEntity):

    def __init__(self):
        self.velocity = None     # 速度
        self.heading = None      # 实体朝向
        self.side = None         # 垂直向量的向量
        self.mass = 10
        self.max_speed = 10
        self.max_force = 0
        self.max_turn_rate = 0


class Vehicle(MovingEntity):
    world = None  # 世界对象
    steering = None # SteeringBehaviors


