from setuptools import setup
setup(
    name='pyteslaapi',
    version='0.0.28',
    packages=['pyteslaapi'],
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    python_requires='>=3',
    license='Apache 2.0',
    description='A library to work with Tesla API.',
    long_description='A library to work with Tesla car API.',
    url='https://github.com/tyamell/pyteslaapi',
    author='Ty Amell',
    author_email='',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
    ],
)
