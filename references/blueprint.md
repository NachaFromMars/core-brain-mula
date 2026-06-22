# CoreBrainMula-TieuTam V1.0 — Blueprint

## Triết Lý

> "Không phải AI nhớ nhiều nhất là AI thông minh nhất.  
> Mà là AI biết nhớ CÁI GÌ và biết CÁI GÌ đang là hiện tại."

### 3 Nguyên Tắc Cốt Lõi
1. **ZERO DECAY** — Mọi memory sống mãi mãi (`decay_rate=0.0`)
2. **CONFLICT INTEL** — Khi trùng lặp: tự quyết (certainty≥0.8) hoặc hỏi (<0.8), luôn thông báo
3. **TOKEN OPTIMAL** — `max_context_tokens=4000`, composite scoring, SimHash dedup

---

## Tại Sao Zero Decay?

NeuralMemory gốc dùng Ebbinghaus curve: `retention = e^(-0.1 × days)`
- Sau 7 ngày: còn 50%
- Sau 30 ngày: còn 5%

Với Tiểu Tâm, đây là anti-pattern vì:
- Henry Rules/Dylan Rules **KHÔNG BAO GIỜ** được phép quên
- Lịch sử quyết định cần được trace lại
- Audit trail cho mọi thay đổi config/tech stack

**Fix:** `decay_rate=0.0` → `math.exp(-0.0 × days) = 1.0` → không decay.

---

## Cơ Chế Conflict (Từ Source Code)

Khi encode memory mới, `ConflictDetectionStep` tự động:
1. Phát hiện neuron mới conflict với neuron cũ
2. Tạo synapse `CONTRADICTS` giữa 2 neurons
3. `ConfirmatoryBoostStep` boost activation neuron mới
4. Neuron cũ bị demote (activation giảm nhẹ, **không xóa**)

**Kết quả:** Cả 2 tồn tại, cái mới dominant, cái cũ accessible khi query sâu.

---

## Composite Scoring (context_optimizer.py)

```python
score = (
    0.30 * activation_level +      # Bao nhiêu lần được recall gần đây?
    0.25 * priority_normalized +   # TypedMemory.priority / 10
    0.20 * frequency_normalized +  # min(access_count / 20, 1.0)
    0.15 * conductivity +          # Fiber pathway strength
    0.10 * freshness_score         # Mới tạo thì bonus nhỏ
)
```

---

## Priority System

| Priority | Type | Rule |
|----------|------|------|
| 10 | instruction, preference | Critical rules — LUÔN trong context |
| 8 | fact (user profiles) | Người dùng quan trọng |
| 7 | decision | Quyết định architecture/tech |
| 5 | insight | Lessons learned |
| 3 | fact (general) | Dates, versions, general info |

---

## Synapse Types (Dùng Cho Audit Trail)

| Type | Ý nghĩa |
|------|---------|
| `CONTRADICTS` | Memory A mâu thuẫn Memory B |
| `CAUSED_BY` | Effect ← Cause |
| `LEADS_TO` | Cause → Effect |
| `RESOLVED_BY` | Bug/issue ← Fix |
| `BEFORE/AFTER` | Timeline |
| `RELATED_TO` | Liên quan chung |

---

## Roadmap

### V1.0 (Current)
- Zero decay config
- Import MEMORY.md
- Conflict Intelligence Protocol
- Token Budget 4,000

### V1.1 (1 tháng sau)
- Tune composite scoring dựa trên usage patterns
- Auto-categorize memories by topic cluster
- Brain stats dashboard

### V2.0 (Tương lai)
- Multi-brain support (1 brain/project)
- Cross-brain spreading activation
- Bidirectional MEMORY.md sync
- Proactive memory surfacing

---

## File Structure

```
skills/core-brain-mula/
├── SKILL.md                     ← Instructions chính
├── scripts/
│   ├── setup.py                 ← Cài đặt + config
│   ├── import_memory.py         ← Import MEMORY.md → brain
│   ├── conflict_resolver.py     ← Conflict assessment helper
│   └── health_backup.py         ← Daily health check + backup
└── references/
    ├── blueprint.md             ← File này
    ├── import-guide.md          ← Hướng dẫn import chi tiết
    └── conflict-examples.md     ← Ví dụ resolve conflict thực tế
```
