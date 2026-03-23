.PHONY: all test lint format docs-serve docs-build

all: test lint

test:
	@echo "Running tests..."
	@python3 tests/test_review_command.py

docs-serve:
	@mkdocs serve

docs-build:
	@mkdocs build

install-hooks:
	ln -sf ../../.gemini/hooks/pre-commit.py .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
