#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import argparse

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text, color):
    """Print text with color"""
    print(f"{color}{text}{Colors.ENDC}")

def print_step(step_num, description):
    """Print a step header"""
    print_colored(f"\n[Step {step_num}] {description}", Colors.HEADER + Colors.BOLD)

def print_success(text):
    """Print a success message"""
    print_colored(f"✓ {text}", Colors.GREEN)

def print_error(text):
    """Print an error message"""
    print_colored(f"✗ {text}", Colors.RED)

def print_warning(text):
    """Print a warning message"""
    print_colored(f"! {text}", Colors.YELLOW)

def run_command(cmd, cwd=None, shell=True):
    """Run a shell command and return the result"""
    print_colored(f"Running: {cmd}", Colors.CYAN)
    try:
        process = subprocess.Popen(
            cmd, 
            shell=shell, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=cwd,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print_error(f"Command failed with exit code {process.returncode}")
            print_error(f"Error: {stderr}")
            return False, stdout, stderr
        
        return True, stdout, stderr
    except Exception as e:
        print_error(f"Exception while running command: {e}")
        return False, "", str(e)

def is_git_installed():
    """Check if git is installed"""
    success, _, _ = run_command("git --version", shell=True)
    return success

def is_uv_installed():
    """Check if uv is installed"""
    success, _, _ = run_command("uv --version", shell=True)
    return success

def clone_repository(repo_url, target_dir, branch=None):
    """Clone a git repository"""
    if os.path.exists(target_dir):
        print_warning(f"Directory {target_dir} already exists. Skipping clone.")
        if branch:
            # Try to checkout the branch
            success, _, _ = run_command(f"git checkout {branch}", cwd=target_dir)
            if success:
                print_success(f"Checked out branch {branch}")
            else:
                print_error(f"Failed to checkout branch {branch}")
        return True
    
    cmd = f"git clone {repo_url} {target_dir}"
    success, _, _ = run_command(cmd)
    
    if not success:
        return False
    
    if branch:
        success, _, _ = run_command(f"git checkout {branch}", cwd=target_dir)
        if not success:
            print_error(f"Failed to checkout branch {branch}")
            return False
    
    return True

def setup_venv(comfy_dir):
    """Set up the virtual environment"""
    success, _, _ = run_command("uv venv", cwd=comfy_dir)
    if not success:
        return False
    
    # Determine the Python executable path based on the platform
    if platform.system() == "Windows":
        python_path = os.path.join(comfy_dir, ".venv", "Scripts", "python.exe")
    else:
        python_path = os.path.join(comfy_dir, ".venv", "bin", "python")
    
    # Ensure pip is installed in the venv
    success, _, _ = run_command(f"{python_path} -m ensurepip --upgrade", cwd=comfy_dir)
    return success

def install_dependencies(comfy_dir):
    """Install dependencies using uv sync"""
    if platform.system() == "Darwin":  # macOS
        cmd = "uv sync --extra cpu"
    else:  # Windows or Linux
        cmd = "uv sync --extra cu126"
    
    success, stdout, stderr = run_command(cmd, cwd=comfy_dir)
    if success:
        print_success("Dependencies installed successfully")
    else:
        print_error(f"Failed to install dependencies: {stderr}")
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Set up ComfyUI for testing custom nodes")
    parser.add_argument("--comfy-dir", default="./ComfyUI", help="Directory where ComfyUI will be cloned")
    parser.add_argument("--branch", default="rh-uvtest", help="Branch to checkout for ComfyUI")
    parser.add_argument("--skip-clone", action="store_true", help="Skip cloning repositories")
    parser.add_argument("--skip-venv", action="store_true", help="Skip creating virtual environment")
    parser.add_argument("--skip-deps", action="store_true", help="Skip installing dependencies")
    
    args = parser.parse_args()
    
    # Convert to absolute path
    comfy_dir = os.path.abspath(args.comfy_dir)
    
    print_colored("ComfyUI Custom Node Testing Setup", Colors.HEADER + Colors.BOLD)
    print_colored("=" * 50, Colors.HEADER)
    print(f"Platform: {platform.system()}")
    print(f"ComfyUI directory: {comfy_dir}")
    print(f"Branch: {args.branch}")
    print_colored("=" * 50, Colors.HEADER)
    
    # Check prerequisites
    if not is_git_installed():
        print_error("Git is not installed. Please install Git and try again.")
        return 1
    else:
        print_success("Git installed successfully")
    
    if not is_uv_installed():
        print_error("uv is not installed. Please install uv and try again.")
        print_warning("You can install uv with: pip install uv")
        return 1
    else:
        print_success("uv installed successfully")
    
    # Step 1: Clone ComfyUI repository
    if not args.skip_clone:
        print_step(1, "Cloning ComfyUI repository")
        if not clone_repository("https://github.com/comfyanonymous/ComfyUI", comfy_dir, args.branch):
            print_error("Failed to clone ComfyUI repository")
            return 1
        print_success("ComfyUI repository cloned successfully")
    
    # Step 2: Clone ComfyUI-Manager repository
    if not args.skip_clone:
        print_step(2, "Cloning ComfyUI-Manager repository")
        manager_dir = os.path.join(comfy_dir, "custom_nodes", "ComfyUI-Manager")
        # Create custom_nodes directory if it doesn't exist
        os.makedirs(os.path.dirname(manager_dir), exist_ok=True)
        if not clone_repository("https://github.com/ltdrdata/ComfyUI-Manager", manager_dir):
            print_error("Failed to clone ComfyUI-Manager repository")
            return 1
        print_success("ComfyUI-Manager repository cloned successfully")
    
    # Step 3: Create virtual environment
    if not args.skip_venv:
        print_step(3, "Creating virtual environment")
        if not setup_venv(comfy_dir):
            print_error("Failed to create virtual environment")
            return 1
        print_success("Virtual environment created successfully")
    
    # Step 4: Install dependencies
    if not args.skip_deps:
        print_step(4, "Installing dependencies")
        if not install_dependencies(comfy_dir):
            print_error("Failed to install dependencies")
            return 1
        print_success("Dependencies installed successfully")
    
    # Final message
    print_colored("\nSetup completed successfully!", Colors.GREEN + Colors.BOLD)
    print_colored("=" * 50, Colors.GREEN)
    
    # Determine the Python executable path based on the platform
    if platform.system() == "Windows":
        python_path = os.path.join(comfy_dir, ".venv", "Scripts", "python.exe")
    else:
        python_path = os.path.join(comfy_dir, ".venv", "bin", "python")
    
    print_colored("Next steps:", Colors.CYAN)
    print("1. Run the test script: uv run main.py")
    print_colored("=" * 50, Colors.GREEN)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
