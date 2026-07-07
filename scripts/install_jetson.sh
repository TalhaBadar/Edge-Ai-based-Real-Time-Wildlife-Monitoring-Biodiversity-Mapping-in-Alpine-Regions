#!/usr/bin/env bash
set -e
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-jetson.txt

echo "Jetson dependencies installed. Make sure PyTorch/TorchVision versions match your JetPack version."
