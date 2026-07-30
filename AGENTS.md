# Codex AGENTS

## Purpose

This repository is a calculation-free, static catalog for the Wald inference applet portfolio.
`data/tools.json` is the source of truth for public tool metadata.

## Commands

- Setup: `uv sync --locked`
- Format: `make fmt`
- Verification: `make verify`
- Public metadata check: `make live-check`
- Local server: `make serve`

## Rules

- Do not add statistical formulas, Pyodide, telemetry, persistence, or input-bearing links.
- Do not mark an app validated without completed evidence.
- Do not duplicate manifest versions or URLs in rendered card markup.
- Keep observed-data conditioning distinct from assumed-truth design conditioning.
- Preserve semantic HTML, keyboard focus, text alternatives, and mobile readability.
- Use `apply_patch` for hand-authored edits and run the full verification matrix.
