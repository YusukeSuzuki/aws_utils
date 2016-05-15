#!/usr/bin/env python3
from setuptools import setup

setup(
    name='aws_utils',
    version='0.1.0',
    description='Tools for managing AWS service. It\'s for my own use.',
    url='http://github.com/YusukeSuzuki/aws_utils',
    author='Yusuke Suzuki',
    author_email='public@geekfield.jp',
    license='MIT',
    packages=['aws_utils'],
    scripts=[
        'bin/ec2',
        'bin/ec2_ssh_priv'
        ],
    install_requires=[
        'boto3'
        ],
    zip_safe=False
    )

