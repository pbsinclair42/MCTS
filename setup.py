from setuptools import setup

setup(
    name='mcts',
    packages=['mcts'],
    version='1.0.1',
    description='A simple package to allow users to run Monte Carlo Tree Search on any perfect information domain',
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    author='Paul Sinclair',
    author_email='pbsinclair42@gmail.com',
    url='https://github.com/pbsinclair42/MCTS',
    download_url='https://github.com/pbsinclair42/MCTS/archive/1.0.tar.gz',
    keywords=['mcts', 'monte', 'carlo', 'tree', 'search'],
    classifiers=[],
)
