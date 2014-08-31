#!/usr/bin/env python
# encoding: utf-8

from miner import Miner, Wife
from entity import EntityManager

em = EntityManager()

m = Miner('Bob')
w = Wife('Elsa')

em.register_entity(m)
em.register_entity(w)

for i in xrange(200):
    m.update()
    w.update()

