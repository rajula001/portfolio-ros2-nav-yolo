# Gazebo + ROS 2 Jazzy base so vendor plugins are in /opt/ros/jazzy/opt/gz_sim_vendor
FROM ros:jazzy-ros-base

ENV DEBIAN_FRONTEND=noninteractive

# Minimal: ros_gz sim + bridge (vendor plugins included under /opt/ros/jazzy/opt/gz_sim_vendor)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    mesa-utils libegl1 libgbm1 \
  && rm -rf /var/lib/apt/lists/

# Headless rendering env
ENV QT_QPA_PLATFORM=offscreen \
    LIBGL_ALWAYS_SOFTWARE=1 \
    MESA_GL_VERSION_OVERRIDE=3.3

# Resource search path (we’ll also set this in compose)
ENV GZ_SIM_RESOURCE_PATH=/ws/simulation/models:/ws/simulation/worlds

WORKDIR /ws
COPY ../../simulation/ /ws/simulation/
