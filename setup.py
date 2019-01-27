import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="lunchbot",
    version="0.1.0",
    url="https://github.com/lumbric/lunchbot",
    license='MIT',

    author="lumbric",
    author_email="lumbric@gmail.com",

    description="Provide lunch menu information and vote for options via slack integration.",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    entry_points={
        'console_scripts': ['lunchbot = lunchbot.main:main'],
    },

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
