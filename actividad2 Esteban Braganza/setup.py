from setuptools import setup

setup(
    name = 'act_02',
    version = '0.1.1',
    packages = ['act_02'],
    install_requires = ['act_02'],
    entry_points = {
        'console_scripts': ['act_02 = act_02.__main__:main']
    }
)