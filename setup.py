from setuptools import setup, find_packages

setup(
    name="grassroots_function",
    version="0.0.5",
    author="LINGTIAN303",
    author_email="lingtian.303@gmail.com",
    description="使用 OpenAI 的 GPT-3.5-turbo-0613 模型调用函数的软件包",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LINGTIAN303/Grassroots-function",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "openai",
        "requests"
    ],
    python_requires='>=3.6',
)
