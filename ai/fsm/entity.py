class BaseGameEntity(object):

    def set_id(self, id_):
        self.id = id_

    def update(self):
        self.fsm.update()

    def get_fsm(self):
        return self.fsm

    def handle_message(self, receiver, msg):
        return self.fsm.handle_message(self, receiver, msg)


class EntityManager(object):
    _instance = None
    _entities = {}
    _next_id = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EntityManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_entity(self, entity):
        entity.set_id(self.next_id())
        self._entities[entity.id] = entity

    def remove_entity(self, entity):
        self._entities.pop(entity.id)

    def get_entity(self, id_):
        return self._entities[id_]

    def next_id(self):
        self._next_id += 1
        return self._next_id


class Dispatcher(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Dispatcher, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def dispatch(self, sender, receiver, msg, delay=0, extra=None):
        em = EntityManager()
        em.get_entity(receiver).handle_message(em.get_entity(sender), msg)


class OakTree(BaseGameEntity):
    def handle_message(self, sender, msg):
        if msg == 'HitWithAxe':
            print('HitWithAxe')
        elif msg == 'StormyWeather':
            print('StormyWeather')
        return self.fsm.handle_message(sender, msg)


class MovingEntity(BaseGameEntity):

    def __init__(self):
        pass


def vector2normalize(vector):
    return vector.normalize()

def vector2normalize_sq(vector):
    return vector.normalize_sq()

class Vector2(object):
    pass

class StreeringBehaviors(object):

    def seek(self, target_pos):
        desired_velocity = vector2normalize(target_pos - self.vehicle.pos()) * self.vehicle.max_speed
        return desired_velocity - self.vehicle.velocity

    def flee(self, target_pos):
        # only flee if the target is within 'panic distance'
        panic_distance_sq = 100.0 * 100.0
        if (vector2normalize_sq(self.vehicle.pos(), target_pos) > panic_distance_sq):
            return Vector2(0, 0)
        desired_velocity = vector2normalize(self.vehicle.pos() - target_pos) * self.vehicle.max_speed
        return desired_velocity - self.vehicle.velocity

