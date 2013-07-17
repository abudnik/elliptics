#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import random

rnd = random.randint(0, 999999999)
test_id = "test_id_" + str(rnd)
test_ind = "test_ind_" + str(rnd)
test_data = "test_data_" + str(rnd)

sys.path.insert(0, "bindings/python/")
import elliptics

elog = elliptics.Logger("/dev/stderr", 0)
cfg = elliptics.Config()

node = elliptics.Node(elog, cfg)
node.add_remote("localhost", 1025)

s = elliptics.Session(node)
s.set_groups([1])

r = s.set_indexes(s.transform(test_id), [test_ind], [test_data])
r.wait()
assert r.successful()

r = s.find_any_indexes([test_ind])
r.wait()
assert r.successful()
assert len(r.get()) >= 1
assert r.get()[0].indexes[0].data == test_data

r = s.find_all_indexes([test_ind])
r.wait()
assert r.successful()
assert len(r.get()) >= 1
assert r.get()[0].indexes[0].data == test_data

r = s.list_indexes(s.transform(test_id))
r.wait()
assert r.successful()
assert len(r.get()) >= 1
assert r.get()[0].data == test_data


z = s.find_any_indexes_raw([s.transform(test_ind)])
z.wait()
assert z.successful()
assert len(z.get()) >= 1
assert z.get()[0].indexes[0].data == test_data

z = s.find_all_indexes_raw([s.transform(test_ind)])
z.wait()
assert z.successful()
assert len(z.get()) >= 1
assert z.get()[0].indexes[0].data == test_data