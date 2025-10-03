FROM ros:jazzy-ros-base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-robot-localization \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY ../../simulation/config/ekf.yaml /ws/config/ekf.yaml

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_DOMAIN_ID=42
# Starts ekf_node (map->odom or odom->base_link, depending on config)
CMD bash -lc "source /opt/ros/jazzy/setup.bash && ros2 run robot_localization ekf_node --ros-args --params-file /ws/config/ekf.yaml"
