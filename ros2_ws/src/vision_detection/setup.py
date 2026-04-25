from setuptools import setup
import os
from glob import glob
package_name = 'vision_detection'
setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aysha Ahmed',
    maintainer_email='ayshaahmed8642@gmail.com',
    description='RoboCup vision system',
    license='MIT',
    entry_points={
        'console_scripts': [
            'robocup_vision = vision_detection.vision_node:main',
        ],
    },
)
