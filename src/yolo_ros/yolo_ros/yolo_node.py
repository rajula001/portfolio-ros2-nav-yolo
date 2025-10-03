import os, rclpy, torch
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose, BoundingBox2D
from cv_bridge import CvBridge
from ultralytics import YOLO

class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.bridge = CvBridge()
        model_path = os.getenv('YOLO_MODEL', 'yolov8n.pt')
        self.get_logger().info(f'Loading YOLO model: {model_path}')
        self.model = YOLO(model_path)
        self.sub = self.create_subscription(Image, '/camera/image', self.cb, 10)
        self.pub = self.create_publisher(Detection2DArray, '/yolo/detections', 10)
        self.use_sim_time = os.getenv('USE_SIM_TIME', 'true').lower() in ('1','true','yes')

    def cb(self, msg: Image):
        cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model.predict(cv_img, verbose=False)[0]
        detarr = Detection2DArray()
        detarr.header = msg.header
        for b in results.boxes:
            det = Detection2D()
            det.bbox = BoundingBox2D()
            # xywh in pixels
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            cx = (x1 + x2)/2.0; cy = (y1 + y2)/2.0; w = x2 - x1; h = y2 - y1
            det.bbox.center.position.x = float(cx)
            det.bbox.center.position.y = float(cy)
            det.bbox.size_x = float(w); det.bbox.size_y = float(h)
            hyp = ObjectHypothesisWithPose()
            cls_id = int(b.cls[0].item()) if b.cls is not None else -1
            conf = float(b.conf[0].item()) if b.conf is not None else 0.0
            hyp.id = str(cls_id); hyp.score = conf
            det.results.append(hyp)
            detarr.detections.append(det)
        self.pub.publish(detarr)

def main():
    rclpy.init()
    node = YoloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

