from setuptools import setup, find_packages

setup(
    name='Spotify-Latest-Played-to-Bluesky',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',  # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'spotify-latest-played=main:main',  # Replace with your main function
        ],
    },
)