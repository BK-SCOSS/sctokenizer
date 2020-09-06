from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='sctokenizer',
      description='A Source Code Tokenizer',
      author='Ngoc Bui',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email='ngocjr7@gmail.com',
      version='0.0.1', 
      packages=find_packages(),
      python_requires='>=3.6')
