"""
GitMuse setup configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='gitmuse',
    version='1.0.0',
    author='Burhan',
    author_email='iburhanwebb@gmail.com',
    description='AI-powered commit message generator that understands your code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zwayth/gitmuse',
    project_urls={
        'Bug Tracker': 'https://github.com/zwayth/gitmuse/issues',
        'Documentation': 'https://github.com/zwayth/gitmuse#readme',
        'Source Code': 'https://github.com/zwayth/gitmuse',
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    python_requires='>=3.8',
    install_requires=[
        'click>=8.0.0',
        'rich>=13.0.0',
        'aiohttp>=3.8.0',
    ],
    extras_require={
        'openai': ['openai>=1.0.0'],
        'claude': ['anthropic>=0.18.0'],
        'all': ['openai>=1.0.0', 'anthropic>=0.18.0'],
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'gitmuse=gitmuse.cli:main',
        ],
    },
    keywords='git commit ai ml openai claude conventional-commits automation',
    include_package_data=True,
    zip_safe=False,
)
