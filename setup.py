from setuptools import setup

setup(
    name="findtory",
    version="0.1.0",
    py_modules=["findtory"],
    install_requires=[
        "requests",
        "colorama",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "findtory=findtory:main",
        ],
    },
    author="Zex0nfy",
    description="Find any directory from a website",
    url="https://github.com/zex0nfy/Findtory.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
