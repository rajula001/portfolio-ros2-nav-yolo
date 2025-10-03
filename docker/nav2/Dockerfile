FROM ros:jazzy-ros-base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY ../../simulation/config/nav2_params.yaml /ws/nav2_params.yaml

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_DOMAIN_ID=42
CMD bash -lc "source /opt/ros/jazzy/setup.bash && ros2 launch nav2_bringup bringup_launch.py use_sim_time:=true params_file:=/ws/nav2_params.yaml"

