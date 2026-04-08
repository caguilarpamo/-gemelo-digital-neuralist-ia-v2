# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Gemelo Digital Neuralist IA v2** is a multi-agent AI pipeline (using LangChain + Anthropic Claude) that simulates a full software development team for financial systems. Given a plain-text financial requirement, it orchestrates 10 specialized agents sequentially to produce user stories, analysis, architecture, code, QA reports, documentation, deployment scripts, and a final deliverable package.

## Environment Setup

Requires Python 3.11. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/Scripts/activate  # Windows bash
pip install -r requirements.txt
```

Set `ANTHROPIC_API_KEY` in the `.env` file at the project root (already present — do not commit changes to it).

## Running the Application

**CLI mode** (interactive prompt):
```bash
python main.py
```

**Gradio web UI** (generates a public share link):
```bash
python app_gradio.py
```

## Running Tests

```bash
pytest
```

The test suite is minimal (`tools/test_tools.py` currently stubs tests). Add real tests under `tools/` or create a `tests/` directory.

## Architecture

### Agent Pipeline (`graph/workflow.py`)

The core is a linear sequential pipeline — not a LangGraph graph despite the module name. `ejecutar_flujo(requerimiento)` calls each agent in order:

| Step | Agent | Role |
|------|-------|------|
| 0 | `ValidadorAgent` | Gates the pipeline — rejects non-financial inputs |
| 1 | `RequerimientosAgent` | Generates user stories |
| 2 | `AnalistaAgent` | Produces functional analysis from req + stories |
| 3 | `ArquitectoAgent` | Designs system architecture from analysis |
| 4 | `LiderTecnicoAgent` | Creates technical plan from architecture + analysis |
| 5 | `DevAgent` | Generates Python backend code |
| 6 | `QA1Agent` | Validates code against requirements |
| 7 | `QA2Agent` | Runs simulated test scenarios |
| 8 | `DocumentadorAgent` | Produces full documentation |
| 9 | `DespliegueAgent` | Generates deployment scripts |
| 10 | `EntregableAgent` | Packages everything into a final deliverable |

### Key Patterns

- **`BaseAgent` (`core/base_agent.py`)**: All agents inherit from this. It wraps `ChatAnthropic` with the configured model and injects the agent's system prompt before the user input. Agents with custom input shapes (e.g., `AnalistaAgent`) override `run()` to combine multiple inputs before calling `super().run()`.

- **`ValidadorAgent`**: The only agent that raises an exception to halt the pipeline — it checks for `"RECHAZADO"` in the LLM response.

- **Model config (`config/settings.py`)**: Single source of truth for `MODEL` (`claude-sonnet-4-5`), `MAX_TOKENS` (1500), and `ANTHROPIC_API_KEY`. Change the model here to affect all agents.

- **Financial validation (`validators/financial_rules.py`)**: Static rule checker that flags `float` usage, absence of `Decimal`, and missing transaction handling in generated code.

### Adding a New Agent

1. Create `agents/your_agent.py` inheriting from `BaseAgent`.
2. Define a `PROMPT` string with the agent's role and constraints.
3. Add an instance and call it in `graph/workflow.py`'s `ejecutar_flujo`.
4. Add its output key to the returned dict and to `app_gradio.py`'s output list.
