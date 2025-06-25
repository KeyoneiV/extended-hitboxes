import setuptools

# Read the contents of the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extended-hitboxes",  # This is the name your package will be installed as
    version="0.1.0",           # Start with 0.1.0 as a first release
    author="Keyonei Victory",
    author_email="your.email@example.com", # Replace with your actual email
    description="A lightweight and extensible 2D collision detection library for Pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeyoneiV/extended-hitboxes", # This should be your GitHub repo URL
    packages=setuptools.find_packages(), # Automatically finds your 'collision_lib' package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha", # Indicates it's in early development
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Pygame",
    ],
    python_requires='>=3.7', # Specify the minimum Python version required
    install_requires=[
        "pygame>=2.0.0", # Specify Pygame as a dependency
    ],
    keywords="pygame collision hitbox 2d game-development library",
)