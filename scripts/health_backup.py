#!/usr/bin/env python3
"""
CoreBrainMula-TieuTam V1.0 — Daily Health Check & Backup
Chạy mỗi ngày: kiểm tra brain health, backup, báo cáo.
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path.home() / ".openclaw/workspace/backups/brain"

def run(cmd: str) -> tuple[int, str]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr

def get_brain_stats() -> dict:
    """Lấy thống kê brain."""
    _, output = run("nmem stats --json")
    try:
        return json.loads(output)
    except:
        return {"raw": output}

def backup_brain() -> str:
    """Backup brain ra file JSON."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    backup_path = BACKUP_DIR / f"brain-{date_str}.json"
    
    code, _ = run(f"nmem brain export -o {backup_path}")
    
    if code == 0:
        # Xóa backups cũ hơn 30 ngày
        run(f"find {BACKUP_DIR} -name 'brain-*.json' -mtime +30 -delete")
        return str(backup_path)
    return ""

def health_check() -> dict:
    """Chạy health check."""
    code, output = run("nmem brain health")
    return {"ok": code == 0, "output": output}

def verify_critical_memories() -> dict:
    """Verify các critical memories vẫn còn đủ."""
    critical_checks = [
        ("Henry Rules", "henry"),
        ("Anh Nấng", "naung"),
        ("Lab Ai group", "messaging"),
        ("VaultCore", "vaultcore"),
    ]
    
    results = {}
    for query, key in critical_checks:
        code, output = run(f'nmem recall "{query}" --depth 1')
        results[key] = {
            "ok": code == 0 and len(output) > 50,
            "found": len(output) > 50
        }
    
    return results

def main():
    print("=" * 50)
    print(f"CoreBrainMula Health Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # 1. Health check
    print("\n[1] Brain Health...")
    health = health_check()
    print("  ✅ OK" if health["ok"] else "  ❌ Issues detected")
    if not health["ok"]:
        print(f"  {health['output'][:200]}")
    
    # 2. Stats
    print("\n[2] Stats...")
    stats = get_brain_stats()
    if "raw" in stats:
        print(f"  {stats['raw'][:200]}")
    else:
        for k, v in stats.items():
            print(f"  {k}: {v}")
    
    # 3. Verify critical memories
    print("\n[3] Critical Memory Check...")
    checks = verify_critical_memories()
    all_ok = True
    for key, result in checks.items():
        icon = "✅" if result["ok"] else "❌"
        print(f"  {icon} {key}")
        if not result["ok"]:
            all_ok = False
    
    if not all_ok:
        print("  ⚠️  Một số critical memories không recall được!")
        print("     Chạy: python3 scripts/import_memory.py để re-import")
    
    # 4. Backup
    print("\n[4] Backup...")
    backup_path = backup_brain()
    if backup_path:
        print(f"  ✅ Backup: {backup_path}")
    else:
        print("  ⚠️  Backup failed")
    
    print("\n" + "=" * 50)
    status = "✅ Healthy" if (health["ok"] and all_ok) else "⚠️  Needs attention"
    print(f"Status: {status}")
    print("=" * 50)
    
    return 0 if (health["ok"] and all_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
