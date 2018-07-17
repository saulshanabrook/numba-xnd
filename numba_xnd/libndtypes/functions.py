import llvmlite.ir

import numba.extending
from numba.targets.listobj import ListInstance
from numba.targets.imputils import impl_ret_new_ref
from numba import cgutils
import numba.types

from . import structs
from ..shared import ptr, int_, i64, wrap_c_func


ndt_as_ndarray = wrap_c_func(
    "ndt_as_ndarray",
    numba.types.int32,
    (structs.ndt_ndarray_type, structs.ndt_type, structs.ndt_context_type),
)


@numba.extending.intrinsic
def shape_to_list(typingctx, shape_t, n_t):
    if shape_t != structs.shape_type or n_t != numba.types.int32:
        return

    list_type = numba.types.List(numba.types.int64)
    sig = list_type(structs.shape_type, numba.types.int32)

    def codegen(context, builder, sig, args):
        array, ndim = args
        ndim = builder.sext(ndim, i64)
        inst = ListInstance.allocate(context, builder, list_type, ndim)
        inst.size = ndim
        # print(array.type)
        with cgutils.for_range(builder, ndim) as loop:
            i = loop.index
            inst.setitem(
                idx=i,
                val=builder.load(builder.gep(array, [i])),
                incref=True,  # no idea what incref does
            )

        return impl_ret_new_ref(context, builder, list_type, inst.value)

    return sig, codegen