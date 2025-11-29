#!/usr/bin/env bash
set -e
echo "=== BlindAssist model setup script ==="

# Create models dir
mkdir -p models

# Option A: Export YOLOv8n to ONNX using ultralytics (recommended)
echo "Installing ultralytics (may take a while)..."
python3 -m pip install --upgrade pip
python3 -m pip install ultralytics onnx onnxruntime torch --quiet

echo "Exporting yolov8n to ONNX (yolov8n.pt will be auto-downloaded by ultralytics)..."
python3 - <<'PY'
from ultralytics import YOLO
m=YOLO('yolov8n.pt')
m.export(format='onnx', imgsz=640, opset=12, simplify=True, file='models/yolov8n.onnx')
print('Exported models/yolov8n.onnx')
PY

# Option B: Download MobileFaceNet pretrained weights (if available) and convert to ONNX
echo "Attempting to download MobileFaceNet pretrained weights..."
WEIGHT_URL="https://github.com/foamliu/MobileFaceNet/releases/download/v1.0/mobilefacenet.pt"
wget -q --show-progress -O models/mobilefacenet.pt "$WEIGHT_URL" || echo "Could not download mobilefacenet.pt from releases, please download manually to models/mobilefacenet.pt"

if [ -f models/mobilefacenet.pt ]; then
  echo "Converting MobileFaceNet .pt to ONNX (requires torch and mobilefacenet code)."
  # try to download repository if not present
  if [ ! -d mobilefacenet_repo ]; then
    git clone https://github.com/foamliu/MobileFaceNet.git mobilefacenet_repo || echo "Could not clone MobileFaceNet repo; convert manually."
  fi
  if [ -f mobilefacenet_repo/mobilefacenet.py ]; then
    python3 - <<'PY'
import torch
import sys
sys.path.append('mobilefacenet_repo')
from mobilefacenet import MobileFaceNet
model = MobileFaceNet(512)
ckpt = torch.load('models/mobilefacenet.pt', map_location='cpu')
model.load_state_dict(ckpt)
model.eval()
dummy = torch.randn(1,3,112,112)
torch.onnx.export(model, dummy, 'models/mobilefacenet.onnx', opset_version=12)
print('Exported models/mobilefacenet.onnx')
PY
  else
    echo "MobileFaceNet repo not available for conversion. Please convert manually using your environment."
  fi
else
  echo "Skipping MobileFaceNet conversion. Place mobilefacenet.pt in models/ and run conversion manually."
fi

echo "Setup complete. Models (if converted) are in the models/ folder."
