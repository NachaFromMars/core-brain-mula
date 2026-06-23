# core-brain-mula — Zero-Decay Neural Memory for OpenClaw

> A neural memory system where neurons never die. Every decision, preference, and instruction persists forever with intelligent conflict resolution and automatic deduplication.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blueviolet)](https://github.com/NachaFromMars)

## Overview
core-brain-mula installs and operates a zero-decay neural memory backend for OpenClaw agents. With `decay_rate=0.0` and `prune_threshold=0.0`, no memory is ever pruned. Conflict resolution uses confidence scoring to auto-resolve high-certainty conflicts or ask the user when uncertain. SimHash deduplication prevents redundant entries, and a 4000-token context budget keeps recall fast. Every new decision or preference is written immediately.

## Features
- **Zero decay** — `decay_rate=0.0`, `prune_threshold=0.0`, all neurons survive
- **Conflict resolution** — certainty ≥ 0.8 → auto-resolve + announce; < 0.8 → ask user; both valid → keep with context tags
- **Auto-remember** — every decision / preference / instruction written immediately
- **SimHash dedup** — no duplicate entries
- **Token budget** — `max_context_tokens=4000` for fast recall

## Usage / Quick Start
```bash
pip install neural-memory[server]
npm install -g @neuralmemory/openclaw-plugin
python3 scripts/setup.py
# restart gateway, then:
python3 scripts/import_memory.py
```

## Trigger Keywords (OpenClaw)
install NeuralMemory, import MEMORY.md, conflict resolution, query memory, backup brain, restore brain

## Related Skills
- [context-budgeting](https://github.com/NachaFromMars/context-budgeting) — context window management
- [memory-tiering](https://github.com/NachaFromMars/memory-tiering) — tiered storage layer

---
Part of the [NachaFromMars](https://github.com/NachaFromMars) OpenClaw skill ecosystem.
