from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/ngocjr7/sctokenizer/issues',
    'Documentation': 'https://github.com/ngocjr7/sctokenizer/blob/master/README.md',
    'Source Code': 'https://github.com/ngocjr7/sctokenizer'
}

setup(name='sctokenizer',
      description='A Source Code Tokenizer',
      author='Ngoc Bui',
      long_description=long_description,
      long_description_content_type="text/markdown",
      project_urls=PROJECT_URLS,
      author_email='ngocjr7@gmail.com',
      version='0.0.7', 
      packages=find_packages(),
      python_requires='>=3.6')
