# BlindAssist - Complete Package (with model setup script)

This package contains the full BlindAssist code and a `setup_models.sh` script which will attempt to:
- install required Python packages (in a virtualenv recommended)
- export a YOLOv8n ONNX model (ultralytics) for object detection
- download a MobileFaceNet pretrained `.pt` and convert it to ONNX (if available)
- install ONNX Runtime and other dependencies

**IMPORTANT:** Model files can be large. The script tries to download and convert models automatically but may require manual steps depending on your system and network.

Usage (recommended):
1. Extract ZIP.
2. Open terminal in the folder.
3. Run: `bash setup_models.sh`

After models are prepared, run `python main.py` to start the system.
