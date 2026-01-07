# Makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= uv run sphinx-build
GIT_ROOT      = $(shell git rev-parse --show-toplevel)
SPHINXDIR     = $(GIT_ROOT)/docs/sphinx
BUILDDIR      = $(SPHINXDIR)/_build

.PHONY: help clean html markdown readme-io docs

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Available targets:"
	@echo "  html      - Build HTML documentation"
	@echo "  markdown  - Build Markdown documentation"
	@echo "  readme-io - Generate readme.io docs with frontmatter"
	@echo "  docs      - Build all (markdown, html, and readme.io)"
	@echo "  clean     - Remove build artifacts"

# Clean build directory
clean:
	rm -rf $(BUILDDIR)
	rm -f *.md

# Build HTML documentation
html:
	@$(SPHINXBUILD) -M html "$(SPHINXDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build Markdown documentation
markdown:
	@$(SPHINXBUILD) -M markdown "$(SPHINXDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@echo "Build finished. The Markdown files are in $(BUILDDIR)/markdown."
	@cp $(BUILDDIR)/markdown/*.md .
	@echo "Markdown files copied to docs/"

# Generate readme.io documentation with YAML frontmatter
readme-io: markdown
	@uv run python scripts/generate_readme_docs.py --source-dir $(BUILDDIR)/markdown --output-dir $(BUILDDIR)/readme-io
	@echo "readme.io docs generated in $(BUILDDIR)/readme-io/"

# Build all documentation
docs: markdown html readme-io
