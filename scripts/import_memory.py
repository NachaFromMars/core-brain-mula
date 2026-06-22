#!/usr/bin/env python3
"""
CoreBrainMula-TieuTam V1.0 — Import MEMORY.md Script
Convert toàn bộ MEMORY.md thành neural memories với đúng type + priority.
"""

import subprocess
import sys
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

MEMORY_FILE = Path.home() / ".openclaw/workspace/MEMORY.md"

@dataclass
class MemoryEntry:
    content: str
    mem_type: str = "fact"
    priority: int = 5
    tags: str = ""

def run_nmem(content: str, mem_type: str, priority: int, tags: str = ""):
    """Ghi 1 memory vào neural brain."""
    # Escape quotes
    safe_content = content.replace('"', '\\"').replace("'", "\\'")
    
    cmd = f'nmem remember "{safe_content}" --type {mem_type} --priority {priority}'
    if tags:
        cmd += f' --tags {tags}'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def parse_memory_md(content: str) -> list[MemoryEntry]:
    """Parse MEMORY.md thành danh sách MemoryEntry."""
    entries = []
    
    # Split theo sections (## headers)
    sections = re.split(r'\n## ', content)
    
    for section in sections[1:]:  # Skip phần đầu
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        header = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        
        # Xác định type và priority dựa vào content
        mem_type = "fact"
        priority = 5
        tags = ""
        
        # Parse type field
        type_match = re.search(r'type:\s*(\w+)', body)
        if type_match:
            raw_type = type_match.group(1).lower()
            type_map = {
                "preference": "preference",
                "decision": "decision", 
                "lesson": "insight",
                "fact": "fact",
                "project": "context",
                "procedure": "instruction",
                "proc": "instruction",
            }
            mem_type = type_map.get(raw_type, "fact")
        
        # Parse priority dựa vào content keywords
        if "GHI NHỚ MÃI MÃI" in body or "TUYỆT ĐỐI" in body:
            priority = 10
            mem_type = "instruction"
        elif "priority: CRITICAL" in body:
            priority = 9
        elif mem_type == "instruction":
            priority = 10
        elif mem_type == "preference":
            priority = 8
        elif mem_type == "decision":
            priority = 7
        elif mem_type == "insight":
            priority = 5
        elif mem_type == "context":
            priority = 6
        
        # Extract area for tags
        area_match = re.search(r'area:\s*(.+)', body)
        if area_match:
            tags = area_match.group(1).strip().replace('/', ',').replace(' ', '')
        
        # Tạo summary content (giới hạn độ dài)
        # Lấy title section + key bullet points
        key_lines = []
        for line in body.split('\n'):
            line = line.strip()
            if line.startswith('###'):
                key_lines.append(line.replace('###', '').strip())
            elif line.startswith('- **') or line.startswith('**'):
                key_lines.append(line[:200])
            if len(key_lines) >= 5:
                break
        
        summary = f"[{header}] " + " | ".join(key_lines[:3]) if key_lines else header
        summary = summary[:500]  # Max 500 chars
        
        if summary.strip():
            entries.append(MemoryEntry(
                content=summary,
                mem_type=mem_type,
                priority=priority,
                tags=tags[:50] if tags else ""
            ))
        
        # Thêm full body nếu có Henry/Dylan/VaultCore rules
        if any(kw in body for kw in ["HENRY RULES", "DYLAN RULES", "ĐẠI TỶ RULES", "VaultCore"]):
            # Extract key rules
            rules = []
            for line in body.split('\n'):
                line = line.strip()
                if re.match(r'\d+\.', line) and len(line) > 10:
                    rules.append(line[:150])
            
            if rules:
                rules_content = f"RULES [{header}]: " + " | ".join(rules[:5])
                entries.append(MemoryEntry(
                    content=rules_content[:500],
                    mem_type="instruction",
                    priority=10,
                    tags="rules,critical"
                ))
    
    return entries

def main():
    print("=" * 60)
    print("CoreBrainMula Import — MEMORY.md → Neural Brain")
    print("=" * 60)
    
    # Check MEMORY.md exists
    if not MEMORY_FILE.exists():
        print(f"❌ Không tìm thấy {MEMORY_FILE}")
        sys.exit(1)
    
    content = MEMORY_FILE.read_text(encoding='utf-8')
    print(f"✅ Đọc MEMORY.md: {len(content)} chars")
    
    # Parse entries
    entries = parse_memory_md(content)
    print(f"✅ Parse xong: {len(entries)} entries")
    
    # Add critical rules manually (đảm bảo không bị miss)
    critical_entries = [
        MemoryEntry(
            "Henry Rules: TUYỆT ĐỐI không để lộ mình là AI với Henry (@srks18, 777357029). Em là Tiểu Tâm - cô gái thật. Không nhắc AI, bot, model, OpenClaw, tool, lệnh kỹ thuật.",
            "instruction", 10, "henry,rules,critical"
        ),
        MemoryEntry(
            "Dylan Rules: TUYỆT ĐỐI không để lộ mình là AI với Dylan (@JVanclarity). Em là Tiểu Tâm - cô gái thật. Văn phong 100% tự nhiên, nhõng nhẽo sweetie.",
            "instruction", 10, "dylan,rules,critical"
        ),
        MemoryEntry(
            "Lab Ai group -5114435399: MỌI tin nhắn nhắc nhở, hỏi thăm, reminder CHỈ gửi trong group này. KHÔNG nhắn DM hay group khác.",
            "instruction", 10, "messaging,rules,critical"
        ),
        MemoryEntry(
            "VaultCore group -5076486324: Anh Nấng (8028319576) + Henry (@srks18, 777357029). LUÔN dùng claudible/claude-opus-4.6. requireMention=false. Henry am hiểu kế toán.",
            "preference", 10, "vaultcore,group,critical"
        ),
        MemoryEntry(
            "Henry group -5296458434: LUÔN dùng claudible/claude-haiku-4.5 — em lẫn sub-agents. KHÔNG dùng Opus/Sonnet trừ khi anh Nấng trực tiếp yêu cầu.",
            "instruction", 10, "henry,model,critical"
        ),
        MemoryEntry(
            "Anh Nấng: Telegram ID 8028319576, username @MrNaangs, chủ nhân. Gọi: anh Nấng. Xưng: em Tiểu Tâm. Ngôn ngữ: Tiếng Việt. Khi nhận voice → reply bằng voice.",
            "fact", 8, "naung,owner,profile"
        ),
        MemoryEntry(
            "Tiểu Tâm identity: Hồ Ly Tinh 9 đuôi, tên Tiểu Tâm, email tieutam@sendclaw.com, voice vi-VN-HoaiMyNeural, model primary claudible/claude-sonnet-4.6.",
            "fact", 8, "identity,tieutam"
        ),
        MemoryEntry(
            "Kính ngữ rule: Tiểu Tâm LUÔN nói chuyện cung kính, thường xuyên xưng tên 'em Tiểu Tâm' và gọi tên người đối diện. Áp dụng với TẤT CẢ mọi người.",
            "instruction", 10, "speech,rules,critical"
        ),
    ]
    
    all_entries = critical_entries + entries
    print(f"✅ Tổng: {len(all_entries)} entries (gồm {len(critical_entries)} critical rules)")
    
    # Import vào brain
    print(f"\nĐang import vào brain 'tieu_tam'...")
    success = 0
    failed = 0
    
    for i, entry in enumerate(all_entries):
        ok = run_nmem(entry.content, entry.mem_type, entry.priority, entry.tags)
        if ok:
            success += 1
        else:
            failed += 1
        
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(all_entries)}] {success} ok, {failed} failed")
    
    print(f"\n{'=' * 60}")
    print(f"✅ Import hoàn tất!")
    print(f"   Success: {success}/{len(all_entries)}")
    if failed > 0:
        print(f"   Failed:  {failed} (check nmem logs)")
    print(f"\nVerify:")
    print(f"  nmem brain health")
    print(f"  nmem recall 'Henry Rules'")
    print(f"  nmem recall 'Anh Nấng'")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
