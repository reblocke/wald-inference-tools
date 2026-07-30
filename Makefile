.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Targets:"
	@echo "  uv-sync          Restore the locked development environment"
	@echo "  fmt              Format Python with Ruff"
	@echo "  fmt-check        Check Python formatting"
	@echo "  lint             Run Ruff lint"
	@echo "  validate         Validate the strict tool manifest and local links"
	@echo "  test             Run non-browser tests"
	@echo "  build-site       Build the exact static Pages artifact"
	@echo "  e2e              Run the Chromium browser suite"
	@echo "  e2e-webkit       Run the WebKit browser suite"
	@echo "  verify           Run all local release gates"
	@echo "  live-check       Check public releases, Pages, and hosted package manifests"
	@echo "  serve            Build and serve the catalog on http://127.0.0.1:8000"

.PHONY: uv-sync
uv-sync:
	uv sync --locked

.PHONY: fmt
fmt:
	uv run ruff format .

.PHONY: fmt-check
fmt-check:
	uv run ruff format --check .

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: validate
validate:
	uv run python scripts/validate_tools_manifest.py
	uv run python scripts/validate_validation_evidence.py
	uv run python scripts/validate_validation_status.py
	uv run python scripts/check_links.py

.PHONY: test
test:
	uv run pytest -q -m "not e2e"

.PHONY: build-site
build-site:
	uv run python scripts/build_site.py

.PHONY: e2e
e2e:
	uv run pytest -q -m e2e \
		--browser chromium \
		--tracing retain-on-failure \
		--video retain-on-failure \
		--screenshot only-on-failure \
		--output test-results

.PHONY: e2e-webkit
e2e-webkit:
	uv run pytest -q -m e2e \
		--browser webkit \
		--tracing retain-on-failure \
		--video retain-on-failure \
		--screenshot only-on-failure \
		--output test-results-webkit

.PHONY: verify
verify: fmt-check lint validate test build-site e2e e2e-webkit
	git diff --check

.PHONY: live-check
live-check:
	uv run python scripts/check_links.py --live

.PHONY: serve
serve: build-site
	uv run python -m http.server --bind 127.0.0.1 --directory site 8000
