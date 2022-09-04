import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="split-image",
    version="1.4.0",
    author="Minas Giannekas",
    author_email="contact@whidev.com",
    description="A package that lets you quickly split an image into rows and columns (tiles).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whiplashoo/split-image",
    project_urls={
        "Bug Tracker": "https://github.com/whiplashoo/split-image/issues",
    },
    entry_points="""
    [console_scripts]
    split-image = split_image.split:main
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Pillow',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
