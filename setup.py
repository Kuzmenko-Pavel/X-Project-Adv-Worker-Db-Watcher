import os
import re

from setuptools import setup, find_packages


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'x_project_adv_worker_db_watcher', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in x_project_adv_worker_db_watcher/__init__.py'
            raise RuntimeError(msg)


install_requires = ['pika==0.13.1',
                    'pytz==2019.3',
                    'sqlalchemy==1.3.15',
                    'psycopg2==2.8.4',
                    'psycopg2-binary==2.8.4',
                    'sqlalchemy-utils==0.36.3',
                    'zope.sqlalchemy==1.1',
                    'trafaret==2.0.2',
                    'trafaret-config==2.0.2',
                    'transaction==3.0.0',
                    'intervals==0.8.1'
                    ]

setup(
    name="X-Project-Adv-Worker-Db-Watcher",
    version=read_version(),
    url="",
    packages=find_packages(),
    package_data={

    },
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    test_suite='x_project_adv_worker_db_watcher.tests',
    entry_points={
        'console_scripts': [
        ],
    }
)
