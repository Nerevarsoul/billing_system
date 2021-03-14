import os

from setuptools import find_packages, setup

REPO_PATH = os.path.abspath(os.path.dirname(__file__))


def get_project_dependencies():
    deps_filepath = os.path.join(REPO_PATH, 'requirements.txt')

    try:
        with open(deps_filepath) as fp:
            return list(fp)
    except OSError:
        raise RuntimeError('Unable to inspect project dependencies')


install_requires = get_project_dependencies()


setup_args = dict(
    name='billing-service',
    version='1.0.0',
    include_package_data=True,
    author='Zabirov Innokentiy',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        run_server=app.application:main
    """,
)
setup(**setup_args)
