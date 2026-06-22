# Import Guide — MEMORY.md → Neural Brain

## Cách Import Tự Động

```bash
python3 skills/core-brain-mula/scripts/import_memory.py
```

Script tự động:
1. Parse từng section trong MEMORY.md
2. Detect type + priority từ content
3. Import vào brain `tieu_tam`
4. Thêm 8 critical entries bắt buộc

## Type Mapping

| MEMORY.md type | nmem type | Priority |
|----------------|-----------|----------|
| preference | preference | 8 |
| decision | decision | 7 |
| lesson | insight | 5 |
| fact | fact | 5 |
| project | context | 6 |
| procedure/proc | instruction | 10 |
| (có "GHI NHỚ MÃI MÃI") | instruction | 10 |
| (có "TUYỆT ĐỐI") | instruction | 10 |

## Import Thủ Công

Nếu muốn import từng entry:

```bash
# Critical rule
nmem remember "Henry Rules: không lộ AI với Henry" \
  --type instruction --priority 10 --tags henry,rules,critical

# User profile  
nmem remember "Anh Nấng: ID 8028319576, @MrNaangs, chủ nhân" \
  --type fact --priority 8 --tags naung,profile

# Dynamic fact (dùng eternal để overwrite khi update)
nmem_eternal "VaultCore tech: Next.js 15, model Opus 4.6"

# Decision với context
nmem remember "Chọn Next.js cho VaultCore vì cần SSR cho SEO" \
  --type decision --priority 7 --tags vaultcore,tech
```

## Verify Sau Import

```bash
nmem recall "Henry Rules"     # Phải trả về full rules
nmem recall "Anh Nấng"        # Phải trả về profile
nmem recall "VaultCore"       # Phải trả về config + history
nmem recall "messaging rules" # Phải trả về Lab Ai group rule
nmem brain health             # Overall health
nmem stats                    # Tổng neurons/synapses
```

## Re-import Khi MEMORY.md Thay Đổi

Script idempotent — chạy lại được nhiều lần:
- Entries trùng → `DedupCheckStep` detect và MERGE (không tạo duplicate)
- Entries mới → tạo neuron mới
- Entries thay đổi → tạo conflict → apply Conflict Protocol

## Backup Brain Trước Khi Import

```bash
nmem brain export -o backups/brain-before-import.json
```
