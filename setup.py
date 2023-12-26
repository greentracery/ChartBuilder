# Simple chartbuilder based on matplotlib library
# Homepage: https://github.com/greentracery/ChartBuilder

from setuptools import setup, find_packages
import chartbuilder as chartbuilder


setup(
    name='ChartBuilder',
    description='Simple chartbuilder based on matplotlib library',
    url="https://github.com/greentracery/ChartBuilder",
    version=chartbuilder.__version__,
    packages=find_packages(),
    install_requires=['matplotlib', 'pillow']
)
