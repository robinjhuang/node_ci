## Instructions 

### Install uv

```
uv sync
```

### Set up ComfyUI directory

```
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
git checkout rh-uvtest
uv venv
.venv/bin/python.exe -m ensurepip

git clone https://github.com/ltdrdata/ComfyUI-Manager custom_nodes
uv sync --extra cpu # for mac
uv sync --extra cu126 # for windows
```

### Run script
```
uv run main.py
```
