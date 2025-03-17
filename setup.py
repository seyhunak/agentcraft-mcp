from setuptools import setup, find_packages

setup(
    name="agentcraft_mcp",
    version="0.1.1",
    author="Seyhun Akyurek",
    author_email="seyhunak@gmail.com",
    description="AgentCraft MCP Server: A secure and scalable AI agent framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seyhunak/agentcraft",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-dotenv",
        "mcp",
        "spacy",
        "spacy-transformers",
        "pyyaml",
        "aiohttp"
    ],
    entry_points={
        "console_scripts": [
            "agentcraft-mcp = agentcraft_mcp.server:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)