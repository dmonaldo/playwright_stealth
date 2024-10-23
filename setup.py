import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="playwright-stealth",
    version="2.0.0",
    author="AtuboDad",
    author_email="lcjasas@sina.com",
    description="playwright stealth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mattwmaster58/playwright_stealth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"playwright_stealth": ["js/*.js", "js/**/*.js"]},
    python_requires=">=3.8",
    install_requires=[
        "playwright",
    ],
    extras_require={
        "test": [
            "pytest",
        ]
    },
)
