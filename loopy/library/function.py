from __future__ import division

__copyright__ = "Copyright (C) 2012 Andreas Kloeckner"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from loopy.kernel.function_interface import ScalarCallable


class MakeTupleCallable(ScalarCallable):
    def with_types(self, arg_id_to_dtype, kernel, callables_table):
        new_arg_id_to_dtype = arg_id_to_dtype.copy()
        for i in range(len(arg_id_to_dtype)):
            if i in arg_id_to_dtype and arg_id_to_dtype[i] is not None:
                new_arg_id_to_dtype[-i-1] = new_arg_id_to_dtype[i]

        return (self.copy(arg_id_to_dtype=new_arg_id_to_dtype,
            name_in_target="loopy_make_tuple"), callables_table)

    def with_descrs(self, arg_id_to_descr, callables_table):
        from loopy.kernel.function_interface import ValueArgDescriptor
        new_arg_id_to_descr = dict(((id, ValueArgDescriptor()),
            (-id-1, ValueArgDescriptor())) for id in arg_id_to_descr.keys())

        return (
                self.copy(arg_id_to_descr=new_arg_id_to_descr),
                callables_table)


class IndexOfCallable(ScalarCallable):
    def with_types(self, arg_id_to_dtype, kernel, callables_table):
        new_arg_id_to_dtype = dict((i, dtype) for i, dtype in
                arg_id_to_dtype.items() if dtype is not None)
        new_arg_id_to_dtype[-1] = kernel.index_dtype

        return (self.copy(arg_id_to_dtype=new_arg_id_to_dtype),
                callables_table)


def loopy_specific_callable_func_id_to_knl_callable_mappers(target, identifier):
    """
    Returns an instance of :class:`InKernelCallable` for the *idenitifer*
    which is not present in *target*, but whose interface is given by
    :mod:`loo.py`. Callables that fall in this category are --

    - reductions leading to function calls like ``argmin``, ``argmax``.
    - callables that have a predefined meaning in :mod:`loo.py` like
      ``make_tuple``, ``index_of``, ``indexof_vec``.
    """
    if identifier == "make_tuple":
        return MakeTupleCallable(name="make_tuple")

    if identifier in ["indexof", "indexof_vec"]:
        return IndexOfCallable(name=identifier)

    from loopy.library.reduction import (
            reduction_func_id_to_in_knl_callable_mapper)
    return reduction_func_id_to_in_knl_callable_mapper(target, identifier)


# vim: foldmethod=marker
