from ultralytics import YOLO

model = YOLO('yolov8s.pt')

#results = model.export(format='engine',imgsz=(736,1280),device=0)
results = model.export(format='engine',imgsz=(736,1280),device="cuda:0", half = True)
#results = model.export(format='engine',imgsz=(736,1280),device="cuda:0", half = True, simplify = True, workspace = 8)