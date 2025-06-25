import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extended-hitboxes",
    version="0.2.2",
    author="Keyonei Victory",
    author_email="vkeyonei@gmail.com",
    description="A lightweight and extensible 2D collision detection library for Pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeyoneiV/extended-hitboxes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.7',
    install_requires=[
        "pygame>=2.0.0",
    ],
    keywords="pygame collision hitbox 2d game-development library",
)
