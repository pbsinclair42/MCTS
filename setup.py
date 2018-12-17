from setuptools import setup

setup(
    name='mcts',
    py_modules=['mcts'],
    version='1.0.3',
    description='A simple package to allow users to run Monte Carlo Tree Search on any perfect information domain',
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    author='Paul Sinclair',
    author_email='pbsinclair42@gmail.com',
    license='MIT',
    url='https://github.com/pbsinclair42/MCTS',
    keywords=['mcts', 'monte', 'carlo', 'tree', 'search'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
