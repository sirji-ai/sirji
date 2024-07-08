from setuptools import setup, find_packages

setup(
    name='sirji-messages',
    version='0.0.29',
    author='Sirji',
    description='Sirji messaging protocol implementation to create, validate and parse messages.',
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
