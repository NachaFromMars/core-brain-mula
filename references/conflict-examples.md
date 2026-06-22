# Conflict Examples — CoreBrainMula V1.0

Ví dụ thực tế cách resolve conflict, dựa trên workflow Tiểu Tâm.

---

## Case 1: Auto-resolve (certainty ≥ 0.8)

**Situation:** Anh Nấng đổi model cho VaultCore

```
Neuron A (2026-02-20): "VaultCore dùng claudible/claude-sonnet-4.6"
Neuron B (2026-03-01): "VaultCore group LUÔN dùng claudible/claude-opus-4.6"
```

**Assessment:**
- Time diff: 9 ngày → time_score = 0.3
- Keyword "LUÔN" = update signal → +0.2
- Semantic overlap "VaultCore" "claudible" "model" → overlap ~0.6 → +0.24
- **Certainty = 0.74** → Hỏi anh

**Thông báo:**
```
🤔 Em thấy 2 version về VaultCore model:
   A: VaultCore dùng sonnet-4.6 (2026-02-20)
   B: VaultCore LUÔN dùng opus-4.6 (2026-03-01)
Anh xác nhận đang dùng cái nào ạ?
```

---

## Case 2: Keep Both (contexts khác nhau)

**Situation:** 2 rules về model cho 2 groups khác nhau

```
Neuron A: "Henry group -5296458434: dùng claude-haiku-4.5"
Neuron B: "VaultCore group -5076486324: dùng claude-opus-4.6"
```

**Assessment:**
- Semantic overlap thấp (group IDs khác nhau) → overlap ~0.2
- **Certainty = 0.08** → Keep both

**Action:** Giữ cả 2, context khác nhau hoàn toàn.
```
✅ Giữ cả 2: haiku cho Henry group, opus cho VaultCore group
```

---

## Case 3: Explicit Update bằng nmem_eternal

**Situation:** Tech stack thay đổi rõ ràng

Khi anh Nấng nói: "VaultCore đổi sang Nuxt.js rồi"

```bash
# Em dùng eternal để overwrite sạch
nmem_eternal "VaultCore frontend: Nuxt.js (đổi từ Next.js 2026-03-15)"
```

**Result:** 1 neuron duy nhất về VaultCore frontend, không có conflict.

---

## Case 4: Historical Query

**Situation:** Anh hỏi về quyết định cũ

Anh: "Tại sao mình không dùng React cho VaultCore?"

Em recall được:
```
Neuron A (2026-02-20): "VaultCore dùng React" [activation: 0.4, demoted]
Neuron B (2026-02-25): "Đổi sang Next.js vì SSR" [activation: 0.9]
Synapse: A --CONTRADICTS--> B
Synapse: B <--CAUSED_BY-- "SSR requirement"
```

**Response:**
```
Hồi 20/2 mình có dùng React (vẫn còn trong history), nhưng 
ngày 25/2 anh Nấng quyết đổi sang Next.js vì cần SSR cho SEO.
Anh muốn review lại quyết định này không?
```

---

## Conflict Resolution Checklist

Khi phát hiện `CONTRADICTS` synapse sau recall:

- [ ] Tính certainty (time diff + keywords + semantic overlap)
- [ ] certainty ≥ 0.8 → tự quyết dùng mới, thông báo anh
- [ ] certainty 0.5-0.8 → hỏi anh xác nhận
- [ ] certainty < 0.5 → giữ cả 2, tag context khác nhau
- [ ] Luôn note "version cũ vẫn trong history"
- [ ] KHÔNG xóa neuron cũ trừ khi anh Nấng yêu cầu
