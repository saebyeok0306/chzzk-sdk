import setuptools


setuptools.setup(
    name="chzzk.py",
    version="0.1.0",
    author="westreed",
    author_email="westreed@naver.com",
    description="An unofficial Python SDK Library for CHZZK",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    url="",
    install_requires=open("requirements.txt", "r", encoding="utf-8").read().splitlines(),
    packages=setuptools.find_packages(),
    python_requires=">=3.11.7",
)
