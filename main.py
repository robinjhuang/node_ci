import json
import subprocess
import datetime
import requests
import time
import os

# Configuration
COMFYUI_DIR = os.path.expanduser("~/ComfyUI")  # Default ComfyUI installation directory
COMFYUI_PORT = 8188  # Default ComfyUI port

COMFYUI_MANAGER_DIR = os.path.join(COMFYUI_DIR, "custom_nodes", "ComfyUI-Manager")

# 1) Prepare list of top 100 custom nodes
TOP_NODES = [
  {
    "id": "comfyui-impact-pack"
  },
  {
    "id": "comfyui-kjnodes"
  },
  {
    "id": "comfyui_essentials"
  },
  {
    "id": "comfyui-videohelpersuite"
  },
  {
    "id": "comfyui-custom-scripts"
  },
  {
    "id": "comfyui-easy-use"
  },
  {
    "id": "comfyui_controlnet_aux"
  },
  {
    "id": "comfyui-impact-subpack"
  },
  {
    "id": "was-node-suite-comfyui"
  },
  {
    "id": "rgthree-comfy"
  },
  {
    "id": "cg-use-everywhere"
  },
  {
    "id": "comfyui-florence2"
  },
  {
    "id": "comfyui_ipadapter_plus"
  },
  {
    "id": "comfyui_layerstyle"
  },
  {
    "id": "comfyui-frame-interpolation"
  },
  {
    "id": "comfyui-reactor"
  },
  {
    "id": "efficiency-nodes-comfyui"
  },
  {
    "id": "ComfyUI-Crystools"
  },
  {
    "id": "comfyui_ultimatesdupscale"
  },
  {
    "id": "comfy-mtb"
  },
  {
    "id": "comfyui-hunyuanvideowrapper"
  },
  {
    "id": "comfyui-advanced-controlnet"
  },
  {
    "id": "comfyui_pulid_flux_ll"
  },
  {
    "id": "comfyui-inspire-pack"
  },
  {
    "id": "derfuu_comfyui_moddednodes"
  },
  {
    "id": "comfyui-jakeupgrade"
  },
  {
    "id": "comfyui-animatediff-evolved"
  },
  {
    "id": "comfyui-detail-daemon"
  },
  {
    "id": "comfyui-mxtoolkit"
  },
  {
    "id": "comfyui-art-venture"
  },
  {
    "id": "comfyui-mixlab-nodes"
  },
  {
    "id": "teacache"
  },
  {
    "id": "comfyui-reactor-node"
  },
  {
    "id": "comfyui-advancedliveportrait"
  },
  {
    "id": "comfyui-wd14-tagger"
  },
  {
    "id": "comfyui_ttp_toolset"
  },
  {
    "id": "wavespeed"
  },
  {
    "id": "comfyui-ic-light"
  },
  {
    "id": "comfyui-dream-project"
  },
  {
    "id": "comfyui_tinyterranodes"
  },
  {
    "id": "comfyui-inpaint-cropandstitch"
  },
  {
    "id": "comfyui_custom_nodes_alekpet"
  },
  {
    "id": "comfyui_instantid"
  },
  {
    "id": "comfyui-inpaint-nodes"
  },
  {
    "id": "comfyui-supir"
  },
  {
    "id": "comfyui-cogvideoxwrapper"
  },
  {
    "id": "comfyui-logic"
  },
  {
    "id": "comfyui-ollama"
  },
  {
    "id": "aigodlike-comfyui-translation"
  },
  {
    "id": "cg-image-picker"
  },
  {
    "id": "comfyui-image-saver"
  },
  {
    "id": "pulid_comfyui"
  },
  {
    "id": "comfyui_patches_ll"
  },
  {
    "id": "comfyui_birefnet_ll"
  },
  {
    "id": "comfyui-liveportraitkj"
  },
  {
    "id": "mikey_nodes"
  },
  {
    "id": "teacachehunyuanvideo"
  },
  {
    "id": "comfyui-inspyrenet-rembg"
  },
  {
    "id": "comfyui_fizznodes"
  },
  {
    "id": "comfyui-3d-pack"
  },
  {
    "id": "comfyui-tooling-nodes"
  },
  {
    "id": "comfyui-mvadapter"
  },
  {
    "id": "bizyair"
  },
  {
    "id": "comfyui-diffusers"
  },
  {
    "id": "comfyui-multigpu"
  },
  {
    "id": "janus-pro"
  },
  {
    "id": "comfyui_faceanalysis"
  },
  {
    "id": "comfyui-depthanythingv2"
  },
  {
    "id": "jovimetrix"
  },
  {
    "id": "sd-dynamic-thresholding"
  },
  {
    "id": "comfyui-automaticcfg"
  },
  {
    "id": "comfyui-post-processing-nodes"
  },
  {
    "id": "comfyui-rmbg"
  },
  {
    "id": "comfyui-brushnet"
  },
  {
    "id": "comfyui-depthflow-nodes"
  },
  {
    "id": "comfyui-lora-auto-trigger-words"
  },
  {
    "id": "comfyui-manager"
  },
  {
    "id": "comfyui_zenid"
  },
  {
    "id": "comfyui_smznodes"
  },
  {
    "id": "controlaltai-nodes"
  },
  {
    "id": "comfyui-imagemetadataextension"
  },
  {
    "id": "comfyui_fill-nodes"
  },
  {
    "id": "comfyui-prompt-reader-node"
  },
  {
    "id": "onebuttonprompt"
  },
  {
    "id": "comfyui-saveimagewithmetadata"
  },
  {
    "id": "comfyui-workspace-manager"
  },
  {
    "id": "comfyui-lama-remover"
  },
  {
    "id": "comfyui-styles_csv_loader"
  },
  {
    "id": "comfyui-image-selector"
  },
  {
    "id": "gguf"
  },
  {
    "id": "comfyui-fluxtrainer"
  },
  {
    "id": "comfyui-denoisechooser"
  },
  {
    "id": "comfyui-layerdiffuse"
  },
  {
    "id": "comfyui_bnb_nf4_loaders"
  },
  {
    "id": "easyanimate"
  },
  {
    "id": "comfyui-propost"
  },
  {
    "id": "comfyui_vlm_nodes"
  },
  {
    "id": "comfyui_slk_joy_caption_two"
  },
  {
    "id": "comfyui-mimicmotionwrapper"
  },
  {
    "id": "comfyui-ic-light-native"
  }
]

# Utility function to run commands in a shell and capture output.
# Returns (return_code, stdout, stderr).
def run_cmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = process.communicate()
    return process.returncode, out.decode("utf-8", errors="replace"), err.decode("utf-8", errors="replace")

def check_node_in_object_info(node_id, object_info):
    """
    Check if a custom node is properly installed by examining the object_info response.
    Looks for entries with python_module starting with 'custom_nodes.<node_id>'
    
    Args:
        node_id: The ID of the custom node to check
        object_info: The parsed JSON response from /object_info endpoint
    
    Returns:
        tuple: (bool, str) - (is_found, details_message)
    """
    found_entries = []
    
    # Look through all nodes in object_info
    for node_name, node_data in object_info.items():
        python_module = node_data.get("python_module", "")
        # Check for exact match or match followed by a dot (indicating a submodule)
        if (python_module == f"custom_nodes.{node_id}"):
            found_entries.append({
                "node_name": node_name,
                "python_module": python_module,
                "category": node_data.get("category", "unknown")
            })
    
    if found_entries:
        details = "Found following entries:\n" + "\n".join(
            f"- Node: {entry['node_name']}, Module: {entry['python_module']}, Category: {entry['category']}"
            for entry in found_entries
        )
        return True, details
    
    return False, "No matching entries found in object_info"

def create_json_result_template(node_name):
    """Initialize a result structure (dict) for the JSON schema."""
    return {
        "node_name": node_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "steps": {
            "freeze_requirements_before_install": {
                "success": False,
                "requirements_list": [],
                "error_message": None
            },
            "install_node_status": {"success": False, "install_log": "", "error_message": None},
            "restart_comfyui_status": {"success": False, "error_message": None},
            "object_info_check": {
                "success": False, 
                "found_in_object_info": False,
                "object_info_details": "",
                "error_message": None
            },
            "uninstall_node_status": {"success": False, "uninstall_log": "", "error_message": None}
        },
        "final_outcome": "PENDING"
    }

def main():
    if not os.path.exists(COMFYUI_DIR):
        print(f"Error: ComfyUI directory not found at {COMFYUI_DIR}")
        print("Please set the correct COMFYUI_DIR at the top of the script")
        return

    results = []

    for node in TOP_NODES:
        node_name = node["id"]
        result_data = create_json_result_template(node_name)

        # --------------------------------------------------------------------
        # STEP 1: Freeze the requirements.txt (before installing node)
        # --------------------------------------------------------------------
        cmd_freeze = "uv pip freeze"
        rc, out, err = run_cmd(cmd_freeze, cwd=COMFYUI_DIR)
        if rc == 0:
            result_data["steps"]["freeze_requirements_before_install"]["success"] = True
            lines = out.strip().split("\n")
            result_data["steps"]["freeze_requirements_before_install"]["requirements_list"] = lines
        else:
            result_data["steps"]["freeze_requirements_before_install"]["error_message"] = err
            result_data["final_outcome"] = "FAILED_FREEZE"
            results.append(result_data)
            continue

        # --------------------------------------------------------------------
        # STEP 2: Install the custom node using Manager
        # --------------------------------------------------------------------
        cmd_install_node = f"uv run custom_nodes/ComfyUI-Manager/cm-cli.py install {node_name}"
        rc, out, err = run_cmd(cmd_install_node, cwd=COMFYUI_DIR)
        if rc == 0:
            result_data["steps"]["install_node_status"]["success"] = True
        else:
            result_data["steps"]["install_node_status"]["error_message"] = err
        result_data["steps"]["install_node_status"]["install_log"] = out + "\n" + err

        if rc != 0:
            result_data["final_outcome"] = "FAILED_INSTALL_NODE"
            results.append(result_data)
            continue

        # --------------------------------------------------------------------
        # STEP 3: Start ComfyUI and wait for it to be ready
        # --------------------------------------------------------------------
        cmd_start_comfyui = "uv run main.py"
        comfy_process = subprocess.Popen(cmd_start_comfyui.split(), cwd=COMFYUI_DIR)
        
        # Wait for ComfyUI to start (max 30 seconds)
        start_time = time.time()
        server_ready = False
        while time.time() - start_time < 60:
            try:
                response = requests.get("http://127.0.0.1:8188/queue", timeout=1)
                if response.status_code == 200:
                    server_ready = True
                    break
            except requests.exceptions.RequestException:
                time.sleep(1)
                continue

        if server_ready:
            result_data["steps"]["restart_comfyui_status"]["success"] = True
        else:
            result_data["steps"]["restart_comfyui_status"]["error_message"] = "Server failed to start within 60 seconds"
            result_data["final_outcome"] = "FAILED_START_COMFY"
            comfy_process.terminate()
            results.append(result_data)
            continue

        # --------------------------------------------------------------------
        # STEP 4: Check object_info to verify custom node installation
        # --------------------------------------------------------------------
        try:
            response = requests.get(f"http://127.0.0.1:{COMFYUI_PORT}/object_info", timeout=5)
            if response.status_code == 200:
                object_info = response.json()
                found, details = check_node_in_object_info(node_name, object_info)
                result_data["steps"]["object_info_check"]["success"] = True
                result_data["steps"]["object_info_check"]["found_in_object_info"] = found
                result_data["steps"]["object_info_check"]["object_info_details"] = details
                result_data["steps"]["object_info_check"]["raw_object_info"] = object_info
            else:
                result_data["steps"]["object_info_check"]["success"] = False
                result_data["steps"]["object_info_check"]["error_message"] = f"Status code {response.status_code}"
        except Exception as e:
            result_data["steps"]["object_info_check"]["success"] = False
            result_data["steps"]["object_info_check"]["error_message"] = str(e)
        finally:
            # Cleanup ComfyUI process
            comfy_process.terminate()
            comfy_process.wait()

        # --------------------------------------------------------------------
        # STEP 5: Uninstall the custom node
        # --------------------------------------------------------------------
        cmd_uninstall_node = f"uv run custom_nodes/ComfyUI-Manager/cm-cli.py uninstall {node_name}"
        rc, out, err = run_cmd(cmd_uninstall_node, cwd=COMFYUI_DIR)
        if rc == 0:
            result_data["steps"]["uninstall_node_status"]["success"] = True
        else:
            result_data["steps"]["uninstall_node_status"]["error_message"] = err
        result_data["steps"]["uninstall_node_status"]["uninstall_log"] = out + "\n" + err

        # --------------------------------------------------------------------
        # Final outcome
        # --------------------------------------------------------------------
        if not result_data["steps"]["object_info_check"]["success"]:
            result_data["final_outcome"] = "FAILED_OBJECT_INFO_CHECK"
        elif not result_data["steps"]["object_info_check"]["found_in_object_info"]:
            result_data["final_outcome"] = "FAILED_NODE_NOT_FOUND"
        else:
            result_data["final_outcome"] = "PASSED"

        # Add to overall results
        results.append(result_data)

    # ------------------------------------------------------------------------
    # Save results to a JSON file
    # ------------------------------------------------------------------------
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_filename = f"comfyui_test_results_{timestamp}.json"
    with open(out_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Test results saved to {out_filename}")

if __name__ == "__main__":
    main()
