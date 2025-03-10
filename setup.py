import io

from setuptools import find_packages, setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="TweetScope", 
    version="1.0.0",  
    description="TweetScope: Extract and analyze tweet content and media", 
    long_description="""TweetScope is a Python package that fetches and processes Twitter post data, including text, images, videos, and hashtags. 
    It helps developers easily retrieve and analyze tweet content with simple API calls.""",
    long_description_content_type="text/markdown",
    packages=find_packages(),  
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "requests"],  
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest", "black"], 
    },
)
