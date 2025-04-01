from setuptools import setup, find_packages

setup(
    name="list4free-scrapers",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.9.0",
        "asyncio>=3.4.3",
    ],
    python_requires=">=3.7",
) 