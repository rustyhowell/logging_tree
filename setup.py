
import setuptools

setuptools.setup(
    name='logging_tree',
    version=0.2,
    author='Rusty Howell',
    author_email='rustyhowell@gmail.com',
    url='https://github.com/rustyhowell/logging_tree',
    description='Display logging tree for debugging',
    keywords='logging',
    long_description='',
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Windows',
        ],
    install_requires=['asciitree'],
    license='MIT',
    py_modules=['logging_tree'],
    packages=[],
)
