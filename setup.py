import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='thonny-shoebot-runner',
    version='0.0.3',
    author='Alexandre Villares',
    description='A plugin to run your Python shoebot bots in Thonny IDE.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/villares/thonny-shoebot-runner',
    packages=['thonnycontrib.thonny_shoebot_runner'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['thonny >= 3.0.0', 'shoebot'],
    python_requires='>=3.7',
)
