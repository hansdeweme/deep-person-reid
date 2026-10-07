import re
import numpy as np
import os.path as osp
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize


def readme():
    with open('README.rst') as f:
        content = f.read()
    return content


def find_version():
    version_file = "torchreid/__init__.py"
    with open(version_file, "r", encoding="utf-8") as file:
        content = file.read()
    match = re.search(
        r"^__version__\s*=\s*['\"]([^'\"]+)['\"]",
        content,
        flags=re.MULTILINE,
    )
    if match is None:
        raise RuntimeError(
            f"Could not find __version__ in {version_file}"
        )
    return match.group(1)

def numpy_include():
    try:
        numpy_include = np.get_include()
    except AttributeError:
        numpy_include = np.get_numpy_include()
    return numpy_include


ext_modules = [
    Extension(
        'torchreid.metrics.rank_cylib.rank_cy',
        ['torchreid/metrics/rank_cylib/rank_cy.pyx'],
        include_dirs=[numpy_include()],
    )
]


def get_requirements(filename='requirements.txt'):
    here = osp.dirname(osp.realpath(__file__))
    with open(osp.join(here, filename), 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires


setup(
    name='torchreid',
    version=find_version(),
    description='A library for deep learning person re-ID in PyTorch',
    author='Kaiyang Zhou',
    license='MIT',
    long_description=readme(),
    url='https://github.com/KaiyangZhou/deep-person-reid',
    packages=find_packages(),
    install_requires=["numpy", "h5py", "Pillow", "six", "scipy", "opencv-python", "matplotlib", "tensorboard", "future", "yacs", "gdown", "imageio",],
    extras_require={"dev": ["flake8", "yapf", "isort==4.3.21", ],},
    keywords=['Person Re-Identification', 'Deep Learning', 'Computer Vision'],
    ext_modules=cythonize(ext_modules)
)
