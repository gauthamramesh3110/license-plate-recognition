from darkflow.net.build import TFNet

options = {
    "model" : "cfg/yolo.cfg",
    "load": "bin/yolo.weights",
    "threshold": 0.1,
    "gpu": 0.0
}
