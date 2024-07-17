from skbuild import setup

setup(
    packages=["mtsespy"],
    package_dir={"": "src"},
    cmake_install_dir="src/mtsespy",
)
