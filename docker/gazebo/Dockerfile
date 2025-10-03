FROM ros:jazzy-ros-base
ENV DEBIAN_FRONTEND=noninteractive

# ---- OSRF Gazebo repo (needed for gz-sim8, plugins, rendering) ----
RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends ca-certificates curl gnupg; \
  mkdir -p /usr/share/keyrings; \
  # NEW key location (the old ubuntu-stable/.../gazebo-archive-keyring.gpg is 404)
  curl -fsSL https://packages.osrfoundation.org/gazebo.gpg \
    -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg; \
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
       https://packages.osrfoundation.org/gazebo/ubuntu-stable noble main" \
    > /etc/apt/sources.list.d/gazebo-stable.list; \
  apt-get update

# ---- Gazebo Sim + ROS-GZ bridge + sensor libs + headless EGL/Mesa ----
RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    libgz-sensors8 \
    libgz-sensors8-imu \
    libgz-sensors8-lidar \
    libgz-sensors8-camera \
    libgz-sensors8-depth-camera \
    libgz-sensors8-rgbd-camera \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    libgz-rendering8 \
    libgz-rendering8-ogre2 \
    libegl1 libgbm1 libgl1-mesa-dri mesa-utils \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
# copy only simulation assets
COPY ../../simulation/ /ws/simulation/

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp \
    ROS_DOMAIN_ID=42 \
    QT_QPA_PLATFORM=offscreen \
    GZ_SIM_RESOURCE_PATH=/ws/simulation/models:/ws/simulation/worlds

# Start gz sim headless, spawn mybot, bring up the bridge
CMD bash -lc '\
  set -euo pipefail; \
  echo "[gazebo] starting server (headless)..."; \
  gz sim -r -s -v 2 /ws/simulation/worlds/empty.sdf --render-engine ogre2 --headless-rendering & \
  sleep 3; \
  echo "[gazebo] spawning robot..."; \
  ros2 run ros_gz_sim create -world empty -file /ws/simulation/models/mybot/mybot.sdf; \
  sleep 2; \
  echo "[gazebo] starting bridge..."; \
  ros2 run ros_gz_bridge parameter_bridge \
    /clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock \
    /camera/image@sensor_msgs/msg/Image@gz.msgs.Image \
    /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan \
    /odom@nav_msgs/msg/Odometry@gz.msgs.Odometry \
    /imu@sensor_msgs/msg/Imu@gz.msgs.IMU \
'
