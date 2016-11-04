"""
A utility to ease grading.
"""

from setuptools import find_packages, setup

package = 'grader_toolkit'
version = '0.1.0'
dependencies = [
    'click',
    'click-repl',
    'ruamel.yaml',
    'six',
    'sqlalchemy',
    'typing'
]

setup(
    name=package,
    version=version,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'py-grtk = grader_toolkit.cli:cli_main'
        ]
    },
)
