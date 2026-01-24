# IVAmini UI — Local Flask Interface

A minimal, synchronous Flask client for the IVAmini reasoning engine.

## Design Philosophy

- **UI is a client, not a brain** — All logic remains in `ivamini.orchestrator.core`
- **Thin presentation layer** — Flask, Jinja2, vanilla JavaScript
- **Easy to inspect** — No framework magic, straightforward request/response
- **Easy to remove** — UI can be deleted without affecting core system

## Running the UI

```bash
cd ivamini_ui
python app.py
```

Then open your browser to: **http://localhost:5000**

## Features

### Main Interface
- **Mode Selector** — QUESTION, REVIEW, or PLAN
- **Input Textarea** — Enter your request
- **Output Display** — Read-only result panel
- **Execute Button** — Submit task (or Ctrl+Enter)

### System Views
- **STATUS Tab** — System configuration and metrics
- **MEMORY Tab** — Session memory with timestamps
  - View all context collected during the session
  - Restart Session button to clear memory

## API Endpoints

All endpoints return JSON responses with `TaskOutput` format:

```json
{
  "task_id": "abc12345",
  "task_type": "QUESTION",
  "status": "SUCCESS",
  "result": { ... },
  "confidence": "LOCAL_LLM_OLLAMA_LLAMA3_1B",
  "duration_ms": 245
}
```

### `POST /api/execute`
Execute a task (QUESTION, REVIEW, or PLAN).

Request:
```json
{
  "mode": "QUESTION",
  "content": "What is algorithmic trading?"
}
```

### `GET /api/status`
Get system status (model, context length, permissions, memory entries, etc.)

### `GET /api/memory`
Get current session memory entries.

### `POST /api/restart`
Restart the session (clear memory, create new Orchestrator instance).

## Architecture

```
ivamini_ui/
├── app.py              # Flask app + API routes
├── templates/
│   └── index.html      # Single-page UI
├── static/
│   ├── style.css       # Minimal responsive styling
│   └── script.js       # Client-side interactions
└── README.md           # This file
```

## Key Files

### `app.py`
- Flask app with 5 endpoints: `/`, `/api/status`, `/api/memory`, `/api/execute`, `/api/restart`
- All business logic delegated to `ivamini.orchestrator.Orchestrator`
- Error handling and JSON responses

### `index.html`
- Single HTML page with two panels
- Left: Input (mode selector, textarea, buttons)
- Right: Output (result display, STATUS/MEMORY tabs)
- Responsive design (stacks on mobile)

### `style.css`
- ~300 lines of vanilla CSS (no frameworks)
- Clean, minimal design with proper contrast
- Responsive grid layout
- Smooth transitions and loading indicator

### `script.js`
- Vanilla JavaScript (no jQuery, React, etc.)
- Fetch API for server communication
- Event listeners for user interactions
- Tab switching and status/memory loading

## Security Notes

- **Local only** — Listens on `127.0.0.1:5000` (not exposed to network)
- **No authentication** — Assumes local use only
- **No persistent storage** — All data in memory (session clears on restart)
- **Read-only output** — UI cannot modify core system

## Extending the UI

To add features:

1. Add route in `app.py` that calls Orchestrator
2. Add frontend code to `index.html` + `script.js`
3. Style in `style.css`

**Never modify core logic** — Keep all reasoning in `ivamini.orchestrator.core`.

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py:
# app.run(port=5001, ...)
```

### LLM Not Configured
- This system does not support local LLM execution.
- System will return an error message if reasoning is attempted.

### Session Not Updating
- Click "Refresh Status" or "Refresh Memory" buttons
- Session persists only during app lifetime
- Restart Flask app to clear session

## Removal

If you want to remove the UI layer:
1. Delete the entire `ivamini_ui/` directory
2. Core system (`ivamini/`) remains fully functional
3. Use CLI interface via `main.py` as before

---

**IVAmini UI v1.0** — Thin client, strong core.
