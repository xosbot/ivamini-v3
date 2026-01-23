# IVAmini Architecture (Canonical)

This repository contains multiple generations of IVAmini code.

## Canonical System (Active)

The active and supported execution path is:

- main.py
- ivamini/orchestrator/core.py
- ivamini/tasks/task.py
- ivamini/agents/analysis_agent.py
- ivamini_ui/

All new development MUST target this path.

## Legacy / Archived Code

The following code belongs to older or experimental implementations
and is NOT part of the active IVAmini system:

- ivamini/memory/store.py
- ivamini/models/task.py
- ivamini/agents/echo_agent.py
- ivamini/agents/tool_agent.py
- ivamini/agents/memory_candidate_agent.py
- ivamini/orchestrator/permission_*

These files are retained for historical reference only.
They must not be imported or modified unless explicitly revived.
