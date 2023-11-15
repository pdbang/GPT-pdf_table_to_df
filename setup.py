from setuptools import setup, find_packages

setup(
    name='gpt_pdf_to_csv',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "tabula-py",
        "pandas",
        "io",
        "openai"
    ],
)
