from setuptools import setup, find_packages
from waldl import __version__

with open("requirements.txt") as requirements_txt:
    requirements = requirements_txt.read().splitlines()


setup(
    name="waldl",
    version=__version__,
    author="d3m0n@demonkingswarn",
    author_email="demonkingswarn@protonmail.com",
    description="A module to download wallpapers.",
    packages=find_packages(),
    url="https://github.com/demonkingswarn/waldl",
    keywords=[
        "waldl",
        "wallhaven",
        "wallpapers",
        "rice"
    ],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        waldl=waldl.__main__:__wal_dl__
    """,
    include_package_data=True,
    )
