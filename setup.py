import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='Timer',  
     version='0.1',
     scripts=['Timer/timer_module.py'] ,
     author="Nadav Oved",
     author_email="nadavo@gmail.com",
     description="A Simple Yet Convenient Timer package for Python 3",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/nadavo/Timer.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
