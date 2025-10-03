FROM ros:jazzy-ros-base
ENV DEBIAN_FRONTEND=noninteractive

# Build tools + ROS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-pip \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    ros-jazzy-vision-msgs \
  && rm -rf /var/lib/apt/lists/*

# Python deps for YOLO (CPU)
RUN pip install --no-cache-dir ultralytics==8.2.103 opencv-python-headless==4.10.0.84 numpy

# Workspace
WORKDIR /ws
COPY ../../src/yolo_ros /ws/src/yolo_ros

# Build your package
RUN . /opt/ros/jazzy/setup.sh && colcon build --symlink-install

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_DOMAIN_ID=42
CMD bash -lc "source /opt/ros/jazzy/setup.bash && source /ws/install/setup.bash && ros2 run yolo_ros yolo_node"

