from setuptools import setup

setup(
    name="django-project-organization",
    version="0.1.0",
    description="Django project",
    author="Ilya",
    packages=[],
    install_requires=open("requirements.txt").read().splitlines(),
)
