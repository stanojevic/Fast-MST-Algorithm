from setuptools import setup

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="fast-mst",
    author="Miloš Stanojević",
    version="0.0.1",
    description='Fast MST Parsing Algorithm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/stanojevic/Fast-MST-Algorithm",
    license='MIT License',
    py_modules=['mst'],
    install_requires=['numpy'],
    classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent",
                ],
)
