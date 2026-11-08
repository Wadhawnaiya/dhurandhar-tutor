# Dhurandhar — Agent-Native Architecture

## Overview

Dhurandhar is an **agent-native** intelligent learning companion organized
around a two-layer plugin model — single-shot **Tools** invoked by the
LLM, and multi-stage **Capabilities** that take over a turn — exposed
through three entry points: CLI, WebSocket API, and Python SDK. All three
enter the durable turn application service before the shared turn engine
routes a normalized context to the selected capability.

## Architecture

```
Entry Points:  CLI (Typer)  |  WebSocket /ws  |  Python SDK
                    ↓                   ↓                   ↓
              ┌─────────────────────────────────────────────────┐
              │          TurnApplicationService                 │
              │   persists, coordinates, and replays turns      │
              └──────────────────────┬──────────────────────────┘
                                     ↓
              ┌─────────────────────────────────────────────────┐
              │       TurnEngine → ChatOrchestrator              │
              │   routes UnifiedContext → selected Capability    │
              │   (defaults to `chat`)                           │
              └──────────┬──────────────┬───────────────────────┘
                         │              │
              ┌──────────▼──┐  ┌────────▼──────────┐
              │ ToolRegistry │  │ CapabilityRegistry │
              │  (Level 1)   │  │   (Level 2)        │
              └──────────────┘  └────────────────────┘
```

`TurnApplicationService` owns durable turn state and replay through the
session store and runtime coordinator. Each execution uses a per-turn
`StreamBus`; the orchestrator emits events, the turn runtime persists them,
and adapters replay them to consumers. Runtime settings live in
`data/user/settings/*.json` — project-root `.env` files are intentionally
ignored.

### Level 1 — Tools

Single-function tools the LLM picks on demand. Eight user-toggleable tools
surface in `/settings/tools`:

| Tool                 | Description                                   |
| -------------------- | --------------------------------------------- |
| `brainstorm`         | Breadth-first idea exploration with rationale |
| `web_search`         | Web search with citations                     |
| `paper_search`       | arXiv preprint search                         |
| `zotero_search`      | Search a configured Zotero library            |
| `reason`             | Dedicated deep-reasoning LLM call             |
| `geogebra_analysis`  | Analyze math images into GeoGebra commands    |
| `imagegen`           | Generate images                               |
| `videogen`           | Generate videos                               |

`USER_TOGGLEABLE_TOOL_NAMES` in `dhurandhar/tools/builtin/__init__.py` is the
authoritative toggle list. Other built-ins are **context-gated** or
capability-owned: `CONFIGURABLE_BUILTIN_TOOL_NAMES` declares the context-gated
surface, while `dhurandhar/agents/_shared/tool_composition.py` owns the mount
rules (`ToolMountFlags`) and the always-available workspace tools. Examples
include `rag`, memory and notebook tools, `read_skill`, deferred MCP/CLI tools,
`exec`, `ask_user`, and mastery navigation. `--tool` selects from the
user-toggleable whitelist; it does not bypass context or capability gates.

### Level 2 — Capabilities

Multi-stage pipelines that own the turn:

| Capability       | Stages                                                |
| ---------------- | ----------------------------------------------------- |
| `chat`           | exploring → responding (single agentic loop, default) |
| `ask_questions`  | responding (chat loop forced through `ask_user`)      |
| `deep_solve`     | responding (chat loop + solve planning tools)         |
| `deep_question`  | ideation → generation                                 |
| `deep_research`  | rephrasing → decomposing → researching → reporting    |
| `visualize`      | analyzing → generating → reviewing (SVG / Chart.js / Mermaid / HTML; or routes to Manim sub-stages via `render_type`) |
| `math_animator`  | concept_analysis → concept_design → code_generation → code_retry → summary → render_output |
| `mastery_path`   | responding (Guided Learning — chat loop + mastery tools, gated per topic type) |
| `immersive_reading` | responding (document- or timestamp-grounded media reading loop) |
| `video_lesson`   | code_generation → render_check → render_output (Remotion lesson played live in the browser, with TTS narration) |

All capabilities converge on `emit_capability_result()` in
`dhurandhar/agents/_shared/capability_result.py` so every turn emits the same envelope
(response payload + `cost_summary` from `UsageTracker`). Status copy and
prompts are i18n'd via `capabilities/prompts/{en,zh}/<name>.yaml`.

## CLI Usage

```bash
# Install from the current dev source checkout
python -m pip install -r requirements/full.txt
python -m pip install -e . --no-deps

# Alternative in 1.7.0: choose one in a separate wheel environment
python -m pip install "dhurandhar[full]"  # Full app, CLI + Web/API
python -m pip install dhurandhar         # Core CLI/SDK (chat + ask_questions)
python -m pip install dhurandhar-cli     # Compatibility alias for core

# Run any capability
dhurandhar run chat "Explain Fourier transform"
dhurandhar run deep_solve "Solve x^2=4" --kb my-kb
dhurandhar run visualize "Animate sine wave" --config render_mode=manim_video

# Interactive REPL
dhurandhar chat
# (inside the REPL: /regenerate or /retry re-runs the last user message)

# Partners (IM-connected companions)
dhurandhar partner list

# Knowledge bases, memory, server
dhurandhar kb list
dhurandhar kb create my-kb --doc textbook.pdf
dhurandhar memory show
dhurandhar serve --port 8001       # API server only
dhurandhar start                   # backend + frontend together
```

Examples beyond core require their owning modules; use `dhurandhar module list`
to inspect installed/enabled/ready states and `dhurandhar plugin list` to discover
registered capabilities and tools. Source Web startup also needs Node.js 22 LTS
and `npm ci --legacy-peer-deps` in `web/`. CLI-only source users can skip frontend
setup, but still need the full Python dependencies. Follow
[Agent Setup](docs-for-dev/AGENT_SETUP.md) for credentials and verification.

## Key Files

| Path                                       | Purpose                              |
| ------------------------------------------ | ------------------------------------ |
| `dhurandhar/runtime/orchestrator.py`        | `ChatOrchestrator` — unified entry   |
| `dhurandhar/runtime/launcher.py`            | Backend + frontend lifecycle / port discovery |
| `dhurandhar/runtime/registry/`              | Tool + Capability registries         |
| `dhurandhar/runtime/bootstrap/builtin_capabilities.py` | Built-in capability class paths |
| `dhurandhar/services/config/runtime_settings.py` | JSON settings + process-env overrides |
| `dhurandhar/services/subagent/`             | Local/remote agent connectors; register each backend in `registry.py` and its model options in `models.py` (Grok CLI uses native `streaming-json`) |
| `dhurandhar/core/stream.py`, `dhurandhar/runtime/stream_bus.py` | StreamEvent protocol + async fan-out |
| `dhurandhar/core/tool_protocol.py`          | `BaseTool` + `ToolDefinition`         |
| `dhurandhar/core/capability_protocol.py`    | `TurnCapability` + `CapabilityManifest` |
| `dhurandhar/core/context.py`                | `UnifiedContext` dataclass            |
| `dhurandhar/tools/builtin/__init__.py`      | All built-in tool wrappers           |
| `dhurandhar/capabilities/`                  | Built-in capability implementations  |
| `dhurandhar/app/`                           | `DhurandharApp` SDK facade + durable application service |
| `dhurandhar_cli/main.py`                    | Typer CLI entry point                |
| `dhurandhar/api/routers/unified_ws.py`      | Unified WebSocket endpoint           |
| `apps/desktop/`                            | Dhurandhar Tutor desktop apps for MacOS and Windows (Electron shell + bundled core; per-target builds in `platforms/`) |

## Dependency Layers

The 1.7.0 layout is modular; 1.6.15 and earlier packages use the
previous layout. Core owns the CLI, SDK and shared runtime; feature wheels must
match its version. `dhurandhar-cli` is a metadata-only compatibility alias.
For development, use source or [local wheels](docs-for-dev/MODULES.md).

Module manifests own dependency groups; generated requirements files support
source, Docker and CI installs. `pyproject.toml` stores extra templates under
`tool.dhurandhar.optional-dependencies`; `build_metadata.py` resolves same-version
wheel pins. Source checkouts expose all modules and install external dependencies
through `requirements/full.txt`, followed by `pip install -e . --no-deps`.
Use the source helper for optional extras rather than installing feature wheels
over the checkout:

```bash
python scripts/install_extras.py partners       # Partner channel SDKs
python scripts/install_extras.py matrix         # Matrix channel without E2EE/libolm
python scripts/install_extras.py matrix-e2e     # Matrix with end-to-end encryption
python scripts/install_extras.py math-animator  # Manim; also needs system LaTeX/ffmpeg
python scripts/install_extras.py dev            # Test / lint tooling
python scripts/install_extras.py all            # Full + Manim + dev dependencies
```

Stop Dhurandhar before module changes. Source supports `module enable/disable`;
wheel environments also support `module install/uninstall`. Upgrading a legacy
`dhurandhar-cli` installation requires uninstalling it before installing the new
packages, preserving the same `DHURANDHAR_HOME`; see the setup guide. Validate
with `python -m pip check`, `dhurandhar module list`, and the setup readiness checks.

## Desktop Release Requirement

Starting with the release after v1.7.1, publish the Intel Mac (`macos-x64`)
DMG together with the Apple Silicon (`macos-arm64`) DMG and Windows installer
and portable ZIP for every version. Wait for the Desktop Release workflow,
including `verify-release`, and verify the downloads on the actual GitHub
Release before reporting completion. If any platform fails, fix and rerun it;
do not silently omit Intel Mac or treat a partial desktop release as complete.
See `apps/desktop/README.md` for the build and publication flow.
