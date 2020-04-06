import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybecker",
    version="0.0.6",
    author="Nicolas Berthel",
    author_email="contact@nicolasberthel.fr",
    install_requires=['pyserial>=3.4'],
    description="pybecker is a library to control becker RF shutters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicolasberthel/pybecker",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Home Automation'
    ],
)
