import logging
from typing import List, NamedTuple
from dataclasses import dataclass, field
import datetime, time
import cv2, torch
import numpy as np
import requests, base64



# API = 'http://192.168.0.25:39391/api'
API = 'http://0.0.0.0:8080/api'
# API = 'http://192.168.0.60:30080/api'

MODEL_PATH = "best.pt"
# DEVICE = "cuda" if not torch.cuda.is_available() else "cpu"
DEVICE = "cpu"


class DetectionConfidance(NamedTuple):
    animal_name: str
    confidance_ratio: float

@dataclass
class DetectionResult:
    detected_at: datetime.datetime
    labels: object
    cord: object
    total_labels: int
    confidences: List[DetectionConfidance] = field(default_factory=list)
    
    def add_confidence(self, animal_name: str, confidance_ratio: float):
        self.confidences.append(DetectionConfidance(animal_name, confidance_ratio))
    

class AnimelDetector():
    
    def __init__(self, trained_model_path, trained_animals: List[str], device: str) -> None:
        self.model = self.load_model(trained_model_path, device)
        self.__trained_animals = trained_animals
        
    @property
    def trained_animal_names(self) -> list:
        return self.__trained_animals
    
        
    def load_model(self, trained_model_path, device):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=trained_model_path, force_reload=True)
        model.conf = 0.60 # NMS confidence threshold
        model.iou = 0.30  # NMS IoU threshold
        
        model.to(device)
        
        return model
    
    def detect_image(self, frame, plot_image: bool = True):
        detected_at = datetime.datetime.now()
        result = self._analyze_result_data(self.model(frame), detected_at)
        detection_ended_at = datetime.datetime.now()
        print(f"Detection took: {(detection_ended_at - detected_at).seconds} seconds")
        
        discovery_threshold = 0.0
        temp_count = 20
        temp_sum = 0.0
        
        if plot_image:
            x_shape = frame.shape[1]
            y_shape = frame.shape[0]
            
            # Image Can have multiple animal:
            for detection_no in range(result.total_labels):
                detection_name = self.trained_animal_names[int(result.labels[detection_no])]
                row = result.cord[detection_no]
                confidance_ratio = row[4].item()
                
                temp_count += 1
                temp_sum += confidance_ratio
                result.add_confidence(animal_name=detection_name, confidance_ratio=confidance_ratio)
                
                self.plot_result(frame=frame, 
                                 animal_name=detection_name,
                                 row=row,
                                 x_shape=x_shape,
                                 y_shape=y_shape, 
                                 confidance=confidance_ratio)
                
        if temp_sum/temp_count > discovery_threshold:
            return result, frame
        return result, None
                
                
    
    @staticmethod
    def _analyze_result_data(results, detected_at: datetime.datetime) -> DetectionResult:
        lables, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        total_labels = len(lables)
        
        return DetectionResult(
            labels=lables, cord=cord, total_labels=total_labels, detected_at=detected_at)
        
    @staticmethod
    def plot_result(frame, animal_name, row, x_shape, y_shape, confidance: float) -> None:
        font_scale = min(1,max(3,int(x_shape/500)))
        font_thickness = min(2, max(10,int(x_shape/50)))
        font_color = (0,255,0)
        
        cv2.rectangle(
            img=frame,
            pt1=(int(row[0].item()*x_shape), int(row[1].item()*y_shape)),
            pt2=(int(row[2].item()*x_shape),int(row[3].item()*y_shape)),
            color=font_color,
            thickness=2
        )
        cv2.putText(
            img=frame,
            text=f"{animal_name}: %0.2f" % confidance,
            org=(int(row[0].item()*x_shape), int(row[1].item()*y_shape) - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=font_scale,
            color=font_color,
            thickness=2
        )
        cv2.putText(
            frame, f"{animal_name}: %0.2f" % confidance, (int(row[0].item()*x_shape), int(row[1].item()*y_shape) - 10),
            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,255,0), font_thickness)
        
        
# def send_data(frame, result: DetectionResult):
    
#     encoded, buffer = cv2.imencode('.jpeg', frame)
#     jpg_as_text = base64.b64encode(buffer)
#     jpg_as_text = buffer.tobytes()
    
#     sensor_data = {
#         'datetime': result.detected_at.strftime("%m/%d/%Y, %H:%M:%S"),
#         'confidances': [(conf.animal_name, float("{:.2f}".format(conf.confidance_ratio))) for conf in result.confidences]
#         }

#     result = requests.post(
#         url=API + "/upload",
#         files={"image": jpg_as_text}
#         # data=sensor_data
#     )
    
#     print(result.json())
    
def send_data(frame, result: DetectionResult):
    
    encoded, buffer = cv2.imencode('.jpeg', frame)
    jpg_as_text = base64.b64encode(buffer)
    jpg_as_text = buffer.tobytes()
    
    sensor_data = {
        # 'datetime': result.detected_at.strftime("%m-%d-%Y, %H:%M:%S"),
        'detected_at': result.detected_at,
        'confidances': [(conf.animal_name, float("{:.2f}".format(conf.confidance_ratio))) for conf in result.confidences]
        }

    result = requests.post(
        url=API,
        files={"image": jpg_as_text},
        data=sensor_data
    )
    
    print(result.json())
        
        
def filter_image(frame):
    kernel = np.array([[-1,-1,-1,-1,-1],
                          [-1,2,2,2,-1],
                          [-1,2,8,2,-1],
                          [-1,2,2,2,-1],
                          [-1,-1,-1,-1,-1]]) / 8.0 # Guassian filter for edge enhancement
    # kernel = np.array([[-1,-1,-1], 
        #                [-1, 9,-1],
        #                [-1,-1,-1]])
    
    frame = cv2.filter2D(frame, -1, kernel)
    frame = cv2.rotate(frame, cv2.ROTATE_180) # Specifiqly for our Sensor Node Camera
    
    return frame

def start_detection(model_path, device):
    capture = cv2.VideoCapture(0)
    capture.set(3, 640)
    capture.set(4, 480)
    
    animal_detector = AnimelDetector(trained_model_path=model_path, trained_animals=['Cat', 'Dog'], device=device)
    
    while True:
        time.sleep(2)
        capture_success, frame = capture.read()
        
        print("..capturing")
        # cv2.imwrite("test.png", frame)
        
        if not capture_success:
            logging.warning(f"Camera Capture failure at {datetime.datetime.now()}")
            continue
        
        result, result_frame = animal_detector.detect_image(frame=filter_image(frame=frame), plot_image=True)
        
        if result_frame is not None:
            send_data(result_frame, result)
            print("caputred..")
            # cv2.imwrite("test_detected.png", result_frame)
        
        if cv2.waitKey(1) == ord('q'):
                break
            
    capture.release()
    cv2.destroyAllWindows()
    
    
    
if __name__ == '__main__':
    start_detection(model_path=MODEL_PATH, device=DEVICE)
        