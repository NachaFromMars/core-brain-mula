---
name: core-brain-mula
description: "CoreBrainMula-TieuTam V1.0 — Zero-Decay Neural Memory System. Cài đặt và vận hành NeuralMemory với zero decay (không bao giờ quên), conflict resolution thông minh (tự quyết/hỏi + thông báo), và token budget tối ưu. Use when: (1) Cài NeuralMemory lần đầu, (2) Import MEMORY.md vào neural brain, (3) Phát hiện conflict memory và cần resolve, (4) Query memory với associative recall, (5) Backup/restore brain, (6) Bất kỳ thao tác nào liên quan đến neural memory system."
---

# CoreBrainMula-TieuTam V1.0

Zero-Decay Neural Memory — không bao giờ quên, biết cái gì là hiện tại.

## Quick Setup

```bash
pip install neural-memory[server]
npm install -g @neuralmemory/openclaw-plugin
python3 skills/core-brain-mula/scripts/setup.py
```

Sau đó restart gateway và chạy import:
```bash
python3 skills/core-brain-mula/scripts/import_memory.py
```

## Core Principles

**Zero Decay:** `decay_rate=0.0`, `prune_threshold=0.0` — mọi neuron sống mãi mãi.  
**Conflict Intel:** Khi phát hiện CONTRADICTS synapse → assess certainty → tự quyết hoặc hỏi.  
**Token Optimal:** `max_context_tokens=4000`, composite scoring, SimHash dedup.

## Conflict Resolution Protocol

Sau mỗi `nmem_recall`, check nếu có conflicts:

```
certainty ≥ 0.8 (timestamp mới hơn + semantic match cao):
→ Tự quyết dùng version mới
→ Thông báo: "📝 Em tự cập nhật [topic]: [cũ] → [mới] (cũ vẫn trong history)"

certainty < 0.8 (mơ hồ, không rõ cái nào current):
→ Hỏi: "🤔 Em thấy 2 version về [topic]: A (ngày X) vs B (ngày Y). Anh dùng cái nào?"

Cả 2 đều đúng (contexts khác nhau):
→ Giữ cả 2, tag context
→ Log: "✅ Giữ cả 2: [A] cho [context X], [B] cho [context Y]"
```

## Ghi Nhớ Tự Động

Mọi quyết định/preference/instruction mới từ anh Nấng → ghi ngay:

```bash
# Rules tuyệt đối (không bao giờ thay đổi)
nmem remember "[rule]" --type instruction --priority 10

# Facts có thể thay đổi → dùng eternal để overwrite
nmem_eternal "[fact hiện tại]"

# Lessons/insights
nmem remember "[lesson]" --type insight --priority 5

# Quyết định + lý do
nmem remember "[quyết định] vì [lý do]" --type decision --priority 7
```

## Recall Trước Khi Trả Lời

Trước mọi câu hỏi về người dùng, config, lịch sử, quyết định:
```bash
nmem recall "[topic]" --depth 2
```
Dùng kết quả để enrich câu trả lời. Nếu có conflicts → áp dụng protocol trên.

## Priority Tiers

| Priority | Loại | Ví dụ |
|----------|------|-------|
| 10 | instruction, preference | Henry Rules, messaging rules |
| 8 | fact (người dùng) | Anh Nấng profile, group IDs |
| 7 | decision | Tech stack, architecture |
| 5 | insight, lesson | Forge lessons, code patterns |
| 3 | fact (general) | Deploy dates, version numbers |

## Daily Operations

```bash
nmem brain health      # Freshness + sensitive scan
nmem stats             # Tổng neurons/synapses
nmem last 10           # 10 memories gần nhất
```

## Update vs Append

- **Static facts** (rules, người dùng): `nmem remember` → append, giữ history
- **Dynamic facts** (tech stack, config): `nmem_eternal` → overwrite, 1 neuron sạch
- **Correction**: `nmem forget "[old]"` rồi `nmem remember "[new]"`

## KHÔNG BAO GIỜ

- Chạy `nmem decay`
- Chạy `nmem consolidate`
- Xóa neuron mà không có lệnh từ anh Nấng

## References

- **Blueprint đầy đủ:** `references/blueprint.md` — kiến trúc, triết lý, roadmap
- **Import guide:** `references/import-guide.md` — cách convert MEMORY.md → nmem
- **Conflict examples:** `references/conflict-examples.md` — ví dụ thực tế resolve conflict
