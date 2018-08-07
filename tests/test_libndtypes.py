import unittest

from ndtypes import ndt

import numba_xnd
from numba import njit

n = ndt("10 * 4 * 4 * int64")


@njit
def get_ndim(x):
    return numba_xnd.pyndtypes.unwrap_ndt_object(x).ndt.ndim


@njit
def get_shape(x):
    a = numba_xnd.libndtypes.create_ndt_ndarray()
    numba_xnd.libndtypes.ndt_as_ndarray(
        a,
        numba_xnd.pyndtypes.unwrap_ndt_object(x).ndt,
        numba_xnd.libndtypes.create_ndt_context(),
    )
    return (a.shape[0], a.shape[1], a.shape[2])


@njit
def is_concrete(x):
    return numba_xnd.libndtypes.ndt_is_concrete(
        numba_xnd.pyndtypes.unwrap_ndt_object(x).ndt
    )


class TestNdt(unittest.TestCase):
    def test_ndim(self):
        self.assertEqual(get_ndim(n), 3)

    def test_shape(self):
        self.assertEqual(get_shape(n), (10, 4, 4))

    def test_is_concrete(self):
        self.assertEqual(is_concrete(n), 1)


class TestNdtWrapper(unittest.TestCase):
    def test_ndim(self):
        @njit
        def get_ndim(t_object_wrapper):
            t_object = numba_xnd.pyndtypes.unwrap_ndt_object(t_object_wrapper)
            t = t_object.ndt
            t_wrapper = numba_xnd.libndtypes.wrap_ndt(t, t_object_wrapper)
            return t_wrapper.ndim

        self.assertEqual(get_ndim(n), 3)

    def test_shape(self):
        @njit
        def get_shape(t_object_wrapper):
            t_object = numba_xnd.pyndtypes.unwrap_ndt_object(t_object_wrapper)
            t = t_object.ndt
            t_wrapper = numba_xnd.libndtypes.wrap_ndt(t, t_object_wrapper)
            return t_wrapper.shape

        self.assertEqual(get_shape(n), (10, 4, 4))
