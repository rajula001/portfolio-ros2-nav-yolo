from setuptools import setup
package_name = 'yolo_ros'
setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[('share/ament_index/resource_index/packages',['resource/' + package_name]),
                ('share/' + package_name, ['package.xml'])],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='YOLOv8 ROS2 node',
    entry_points={'console_scripts': ['yolo_node = yolo_ros.yolo_node:main']},
)

