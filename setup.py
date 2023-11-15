from setuptools import setup, find_packages

setup(
    name='gptable',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        "tabula-py",
        "pandas",
        "openai"
    ],
)
