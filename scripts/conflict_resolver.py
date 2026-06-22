#!/usr/bin/env python3
"""
CoreBrainMula-TieuTam V1.0 — Conflict Resolution Helper
Assess và resolve conflicts trong neural memory.
"""

import subprocess
import json
import sys
from datetime import datetime

def nmem_recall(query: str, depth: int = 2) -> dict:
    """Query neural memory và trả về kết quả."""
    cmd = f'nmem recall "{query}" --depth {depth} --json'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return {"context": result.stdout, "conflicts": []}

def assess_certainty(old_content: str, new_content: str, 
                     old_date: datetime, new_date: datetime) -> float:
    """
    Tính certainty score để quyết định tự quyết hay hỏi.
    Returns: 0.0 - 1.0
    """
    score = 0.0
    
    # Time factor (0.4 weight)
    if new_date > old_date:
        days_diff = (new_date - old_date).days
        time_score = min(days_diff / 30, 1.0)
        score += 0.4 * time_score
    
    # Update signal keywords (0.2 weight)
    update_keywords = ["update", "mới", "đổi", "thay", "sửa", 
                       "correction", "thực ra", "bây giờ", "hiện tại"]
    if any(kw in new_content.lower() for kw in update_keywords):
        score += 0.2
    
    # Semantic overlap approximation (0.4 weight)
    old_words = set(old_content.lower().split())
    new_words = set(new_content.lower().split())
    if old_words and new_words:
        overlap = len(old_words & new_words) / len(old_words | new_words)
        score += 0.4 * overlap
    
    return min(score, 1.0)

def format_conflict_message(topic: str, old_val: str, new_val: str, 
                             certainty: float, auto_resolved: bool) -> str:
    """Format thông báo conflict cho anh Nấng."""
    if auto_resolved:
        return (
            f"📝 Em tự cập nhật **{topic}**:\n"
            f"   Trước: {old_val[:100]}\n"
            f"   Hiện tại: {new_val[:100]}\n"
            f"   _(version cũ vẫn còn trong history)_"
        )
    else:
        return (
            f"🤔 Em thấy 2 version về **{topic}**:\n"
            f"   A: {old_val[:100]}\n"
            f"   B: {new_val[:100]}\n"
            f"Anh xác nhận đang dùng cái nào ạ?"
        )

def resolve_conflict(topic: str, old_content: str, new_content: str,
                     old_date: datetime = None, new_date: datetime = None,
                     notify_channel: str = "-5114435399") -> dict:
    """
    Main conflict resolution function.
    Returns: {"action": "auto|ask|keep_both", "message": str, "certainty": float}
    """
    if old_date is None:
        old_date = datetime.now()
    if new_date is None:
        new_date = datetime.now()
    
    certainty = assess_certainty(old_content, new_content, old_date, new_date)
    
    if certainty >= 0.8:
        # Tự quyết
        msg = format_conflict_message(topic, old_content, new_content, 
                                       certainty, auto_resolved=True)
        return {
            "action": "auto",
            "use": "new",
            "certainty": certainty,
            "message": msg,
            "notify": True
        }
    elif certainty >= 0.5:
        # Hỏi
        msg = format_conflict_message(topic, old_content, new_content,
                                       certainty, auto_resolved=False)
        return {
            "action": "ask",
            "certainty": certainty,
            "message": msg,
            "notify": True
        }
    else:
        # Giữ cả 2 — context khác nhau
        return {
            "action": "keep_both",
            "certainty": certainty,
            "message": f"✅ Giữ cả 2 version về {topic} (contexts khác nhau)",
            "notify": False
        }

if __name__ == "__main__":
    # Test
    print("Conflict Resolution Helper — CoreBrainMula V1.0")
    print("Usage: import và dùng resolve_conflict() trong code")
    
    # Demo
    result = resolve_conflict(
        topic="VaultCore tech stack",
        old_content="VaultCore dùng React",
        new_content="VaultCore đổi sang Next.js vì SSR",
        old_date=datetime(2026, 2, 20),
        new_date=datetime(2026, 3, 1)
    )
    print(f"\nDemo result:")
    print(f"  Action: {result['action']}")
    print(f"  Certainty: {result['certainty']:.2f}")
    print(f"  Message: {result['message']}")
