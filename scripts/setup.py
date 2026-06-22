#!/usr/bin/env python3
"""
CoreBrainMula-TieuTam V1.0 — Setup Script
Cài đặt NeuralMemory với zero decay config cho Tiểu Tâm.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

CONFIG_TOML = """[brain]
default = "tieu_tam"
decay_rate = 0.0
prune_threshold = 0.0
reinforcement_delta = 0.05
activation_threshold = 0.1
max_spread_hops = 4
max_context_tokens = 4000

[auto]
min_confidence = 0.7
detect_decisions = true
detect_errors = true
detect_preferences = true

[lifecycle]
run_decay = false
run_consolidate = false

[shared]
enabled = false
url = ""
api_key = ""
"""

OPENCLAW_PLUGIN_CONFIG = {
    "plugins": {
        "slots": {
            "memory": "neuralmemory"
        }
    }
}

def run(cmd, check=True):
    print(f"  → {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(f"    {result.stdout.strip()}")
    if result.stderr and result.returncode != 0:
        print(f"    ERROR: {result.stderr.strip()}")
    if check and result.returncode != 0:
        sys.exit(1)
    return result

def check_installed(pkg):
    result = subprocess.run(f"pip show {pkg}", shell=True, capture_output=True)
    return result.returncode == 0

def main():
    print("=" * 60)
    print("CoreBrainMula-TieuTam V1.0 — Setup")
    print("=" * 60)

    # 1. Install neural-memory
    print("\n[1/5] Kiểm tra neural-memory...")
    if check_installed("neural-memory"):
        print("  ✅ Đã cài rồi")
    else:
        print("  Đang cài...")
        run("pip install 'neural-memory[server]' -q")
        print("  ✅ Xong")

    # 2. Install OpenClaw plugin
    print("\n[2/5] Kiểm tra OpenClaw plugin...")
    result = subprocess.run("npm list -g @neuralmemory/openclaw-plugin", shell=True, capture_output=True)
    if result.returncode == 0:
        print("  ✅ Đã cài rồi")
    else:
        print("  Đang cài...")
        run("npm install -g @neuralmemory/openclaw-plugin -q")
        print("  ✅ Xong")

    # 3. Write zero decay config
    print("\n[3/5] Ghi config zero decay...")
    config_dir = Path.home() / ".neural-memory"
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / "config.toml"
    config_path.write_text(CONFIG_TOML)
    print(f"  ✅ Config: {config_path}")
    print("     decay_rate = 0.0 ✓")
    print("     prune_threshold = 0.0 ✓")
    print("     max_context_tokens = 4000 ✓")

    # 4. Init brain
    print("\n[4/5] Khởi tạo brain 'tieu_tam'...")
    result = run("nmem brain list", check=False)
    if "tieu_tam" in result.stdout:
        print("  ✅ Brain 'tieu_tam' đã tồn tại")
    else:
        run("nmem brain create tieu_tam", check=False)
        print("  ✅ Tạo brain 'tieu_tam'")
    run("nmem brain use tieu_tam", check=False)
    print("  ✅ Đang dùng: tieu_tam")

    # 5. Patch OpenClaw config
    print("\n[5/5] Patch OpenClaw config (memory slot)...")
    openclaw_config_path = Path.home() / ".openclaw" / "openclaw.json"
    if openclaw_config_path.exists():
        with open(openclaw_config_path) as f:
            config = json.load(f)
        
        if "plugins" not in config:
            config["plugins"] = {}
        if "slots" not in config["plugins"]:
            config["plugins"]["slots"] = {}
        
        config["plugins"]["slots"]["memory"] = "neuralmemory"
        
        with open(openclaw_config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"  ✅ Đã patch: {openclaw_config_path}")
        print("  ⚠️  Cần restart OpenClaw gateway để apply!")
    else:
        print(f"  ⚠️  Không tìm thấy {openclaw_config_path} — patch thủ công sau")

    print("\n" + "=" * 60)
    print("✅ Setup hoàn tất!")
    print("\nBước tiếp theo:")
    print("  1. Restart OpenClaw: openclaw gateway restart")
    print("  2. Import MEMORY.md: python3 scripts/import_memory.py")
    print("  3. Verify: nmem brain health")
    print("=" * 60)

if __name__ == "__main__":
    main()
