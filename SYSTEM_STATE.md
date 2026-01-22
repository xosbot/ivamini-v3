# IVAmini v1.0 — FINAL SYSTEM STATE

**Status:** FROZEN & PRODUCTION-READY  
**Date:** January 22, 2026  
**Core Commit:** `493aef2` (v1.0-local tag)  
**Latest:** `2cc0992` (PHASE 3)  

---

## System Overview

IVAmini is a **disciplined local reasoning engine** with zero execution capability, designed for strategic thinking, risk analysis, and system design.

### Core Architecture

```
User Input
    ↓
[UI: Flask Client] ← (optional, removable)
    ↓
[Orchestrator] ← (central control, owns state)
    ↓
[AnalysisAgent] ← (reasoning only, no execution)
    ↓
[LocalLLM] ← (Ollama llama3.2:1b, configurable)
    ↓
[Results] ← (structured output via TaskOutput)
```

### Three Task Modes

| Mode | Purpose | Output | Memory |
|------|---------|--------|--------|
| **QUESTION** | Get definitions | Brief answer | Writes to session |
| **REVIEW** | Analyze risks | Structured analysis | Writes to session |
| **PLAN** | Design approach | 7-part framework | **Read-only** |

---

## Safety Boundaries (ENFORCED)

✅ **LLM has ZERO execution capability**
- Cannot write files
- Cannot modify memory directly
- Cannot trigger side effects
- Cannot access external APIs

✅ **PLAN mode is deterministic**
- 7-part contract (locked):
  1. Objective
  2. Assumptions
  3. Constraints
  4. Step-by-step plan
  5. Risks
  6. Validation checks
  7. What is NOT being done
- No execution verbs allowed (run, execute, implement, build, start, begin)
- Read-only session memory (no writes)

✅ **Session memory is volatile**
- In-memory only (no disk persistence)
- Clears on restart
- Last 5 entries auto-trimmed
- Read-only for PLAN mode

✅ **Orchestrator owns all state**
- Single source of truth
- Permission checks (if enabled)
- Central task routing
- Memory lifecycle management

---

## Running IVAmini

### CLI Interface
```bash
python main.py
# Then enter commands like:
# [QUESTION] What is X?
# [REVIEW] Analyze risks in Y
# [PLAN] Design Z
# [STATUS]
# [MEMORY]
```

### Flask UI (Optional)
```bash
cd ivamini_ui
python app.py
# Open browser: http://localhost:5000
```

---

## What's Included

### Core System
- `ivamini/orchestrator/` — Central control (frozen)
- `ivamini/agents/` — Analysis agent (reasoning only)
- `ivamini/llm/` — Ollama interface (local, no cloud)
- `ivamini/memory/` — Session store (volatile)
- `ivamini/models/` — Data structures (Task, TaskOutput)
- `ivamini/tools/` — Basic tools (registry, filesystem, internet, system)
- `ivamini/interface/` — CLI & voice input
- `ivamini/logs/` — Execution logging (JSONL)

### UI Layer (Optional)
- `ivamini_ui/app.py` — Flask server (thin client)
- `ivamini_ui/templates/` — HTML interface
- `ivamini_ui/static/` — CSS & JavaScript

### Documentation
- `README.md` — Getting started (to be created)
- `ivamini_ui/README.md` — UI documentation
- `USAGE_NOTES.md` — Friction log template
- This file

---

## Git History

```
2cc0992  [PHASE3] Flask UI — Thin client interface
7f45e11  [PHASE2] PLAN mode deterministic reasoning framework
493aef2  [FREEZE] IVAmini v1.0 — Stable local core
cd61e7f  [MODELS] Add structured output formatting
```

**v1.0-local tag:** Points to `493aef2` (frozen baseline)

---

## Configuration

Default `config.yaml`:
```yaml
environment: dev
logging:
  enabled: true
  level: INFO
permissions:
  default: READ
  allow_destructive: false
voice:
  enabled: false  # Set to true to enable voice input
  require_mode: true
llm:
  backend: ollama
  model: "llama3.2:1b"
workspace:
  path: ivamini/workspace
```

---

## Dependencies

### Core
- `ollama` — Local LLM interface
- `pyyaml` — Configuration
- `python 3.10+`

### UI (Optional)
- `flask` — Web framework
- `jinja2` — Template engine (included with Flask)

---

## Known Limitations

⚠️ **Ollama must be running**
- System fails gracefully if Ollama is unavailable
- Error messages are clear and actionable

⚠️ **Single session per orchestrator instance**
- No session persistence across restarts
- Session memory clears on app restart
- Multiple instances don't share state

⚠️ **No concurrency**
- Synchronous design (intentional)
- One request at a time
- Simpler to reason about, easier to debug

⚠️ **Local only**
- No cloud backend
- No network exposure (localhost only)
- Assumes trusted environment

---

## Extending the System (Guidelines)

### ✅ Safe to Add
- New task modes (follow PLAN contract pattern)
- Additional LLM models (update config)
- New tools (register in ToolRegistry)
- UI enhancements (frontend only)
- Logging improvements

### ❌ DO NOT Add
- Execution capabilities
- File writes from LLM
- Background tasks/automation
- External APIs or cloud services
- Persistent session storage (disk)
- Autonomous decision-making

### How to Add Safely
1. Read existing code first
2. Explain WHY the change is needed
3. Make minimal diffs
4. Preserve existing behavior
5. Update call sites when changing signatures
6. Keep business logic in Orchestrator only

---

## PHASE 4: Pause & Use (Now)

You now have a complete, frozen system. Next step:

**Use IVAmini daily for real work.**

Not for:
- Building more features
- Refactoring
- Optimization

Only for:
- Strategic thinking
- Risk analysis
- System design
- Decision clarity
- Learning complex domains

### Create a Friction Log

Edit `USAGE_NOTES.md` after each session:
- What worked well?
- What felt slow or unclear?
- What did you wish it could do?

This becomes your **v1.1 roadmap** (if v1.1 ever happens).

---

## Success Criteria (How You'll Know It's Working)

✅ You use it for 5+ real tasks  
✅ You stop asking "what should I build next?"  
✅ You start asking "does this actually help me?"  
✅ You've filled USAGE_NOTES.md with real observations  
✅ You feel confident in the reasoning output  
✅ You trust the safety boundaries  

---

## Final Notes

IVAmini is designed for **architects and thinkers**, not for replacing your brain or automating decisions. It's a disciplined reasoning companion.

The core is frozen. The boundaries are firm. The system is trustworthy.

Now use it.

---

**IVAmini v1.0**  
*Disciplined local reasoning. Zero autonomy. Clear boundaries.*
