from setuptools import setup

setup(
	name='glurm',
	version='0.1',
    entry_points = {
        'console_scripts': [
            'grun=glurm.main:run',
            'gqueue=glurm.main:queue',
            'gcancel=glurm.main:cancel',
        ],
    }
)
