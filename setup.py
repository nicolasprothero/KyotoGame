from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Weaponize',
    version='2.0',
    packages=find_packages(),
    package_data={
        '': ['requirements.txt'],
        'weaponize': ['assets/**/*']
    },
    install_requires=[
        'pygame==2.4.0',
    ],
    python_requires='>=3.10.6',
    entry_points={
        'console_scripts': [
            'weaponize = src.main:main'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
