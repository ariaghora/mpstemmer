from setuptools import setup

setup(
    name='mpstemmer',
    version='0.1.0',
    description=('Stemmer for Bahasa Indonesia'),
    author='Aria Ghora Prabono',
    author_email='hello@ghora.net',
    url='https://github.com/ariaghora/mpstemmer',
    license='MIT',
    packages=['mpstemmer'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
    )