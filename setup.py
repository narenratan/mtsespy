from skbuild import setup

setup(
    name="mtsespy",
    version="0.1.0",
    description="Python bindings for ODDSound MTS-ESP",
    author="Naren Ratan",
    license="0BSD",
    packages=["mtsespy"],
    package_dir={"": "src"},
    cmake_install_dir="src/mtsespy",
    python_requires=">=3.7",
)
