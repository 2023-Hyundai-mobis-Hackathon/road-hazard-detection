# road-hazard-detection

Utilising YOLOv5 for road hazard detection

## Single-GPU training

`python train.py --img 1280 --batch 16 --epochs 100 --data custom.yaml --weights yolov5m.pt --cache ram --device 0 --patience 10`

## Multi-GPU training

`python -m torch.distributed.run --nproc_per_node 2 train.py --batch --data custom.yaml --weights yolov5s.pt --device 0,1 --cache ram`

## Inference with detect.py

`python detect.py --weights ../models/best.pt --source ../sample/vid.mp4`
