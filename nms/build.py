import os
import torch
from setuptools import setup, find_packages
from torch.utils.cpp_extension import CppExtension, BuildExtension


sources = ['src/nms.c']
headers = ['src/nms.h']
include_dirs = [os.path.realpath('./src')]
defines = []
with_cuda = False

if torch.cuda.is_available():
    print('Including CUDA code.')
    sources += ['src/nms_cuda.c']
    headers += ['src/nms_cuda.h']
    defines += [('WITH_CUDA', None)]
    with_cuda = True

this_file = os.path.dirname(os.path.realpath(__file__))
print(this_file)
extra_objects = ['src/cuda/nms_kernel.cu.o']
extra_objects = [os.path.join(this_file, fname) for fname in extra_objects]

# ffi = create_extension(
#     '_ext.nms',
#     headers=headers,
#     sources=sources,
#     define_macros=defines,
#     relative_to=__file__,
#     with_cuda=with_cuda,
#     extra_objects=extra_objects
# )

if torch.cuda.is_available():
    enable_gpu = True
else:
    enable_gpu = False

if enable_gpu:
    from torch.utils.cpp_extension import CUDAExtension
    build_extension = CUDAExtension
else:
    build_extension = CppExtension

ext_modules = [
    build_extension(
        'ext.nms',
        include_dirs=include_dirs,
        sources=sources,
        extra_objects=extra_objects,
        # extra_compile_args=['-std=c++11']
    )
]

setup(
    name='ext',
    version='0.1',
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExtension}
)
