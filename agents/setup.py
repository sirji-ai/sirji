from setuptools import setup, find_packages

setup(
    name='sirji-agents',
    version='0.0.41',
    author='Sirji',
    description='Orchestrator, Generic Agent, and Research Agent components of the Sirji AI agentic framework.',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sirji-ai/sirji',
    packages=find_packages(),
    include_package_data=True,  # This includes non-code files specified in MANIFEST.in
    install_requires=[
        x for x in open("./requirements.txt", "r+").readlines() if x.strip()
    ],
    python_requires='>=3.6',
    classifiers=[],
    entry_points={
        'console_scripts': [],
    },
)
