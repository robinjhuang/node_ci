## Instructions 

### Install uv

```
uv sync
```

### Set up ComfyUI directory

```
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
uv venv
.venv/bin/python.exe -m ensurepip
uv run ensurepip
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
uv pip install -r requirements.txt

cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager
cd ComfyUI-Manager
uv pip install -r requirements.txt
cd ../../
```

### Run script
```
uv run main.py
```
