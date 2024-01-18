from setuptools import setup, find_packages

setup(
    name="py-korad-serial",
    py_modules=["koradserial"],
    version="0.1.0",  # You can specify an appropriate version number
    description="Python interface for controlling Korad KAxxxxP series power supplies which support the serial modbus protocol.",
    url="https://github.com/starforgelabs/py-korad-serial",
    author="Starforge Labs",
    packages=find_packages(),
    install_requires=[
        "serial"
        # Add dependencies here. For instance, if the project depends on 'requests' you can add 'requests' to this list
    ],
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
