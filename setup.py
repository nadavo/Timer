import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
     name='syct',
     version='0.4.3',
     author="Nadav Oved",
     author_email="nadavo@gmail.com",
     description="A Simple Yet Convenient Timer module for Python 3",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/nadavo/Timer.git",
     package_dir={"": "src"},
     packages=setuptools.find_packages(where="src", exclude=["tests"]),
     python_requires='>=3',
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
