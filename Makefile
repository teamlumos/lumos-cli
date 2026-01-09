# Makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= uv run sphinx-build
GIT_ROOT      = $(shell git rev-parse --show-toplevel)
SPHINXDIR     = $(GIT_ROOT)/docs/src
BUILDDIR      = $(SPHINXDIR)/_build

.PHONY: help clean html markdown readmeio docs

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Available targets:"
	@echo "  html      - Build HTML documentation"
	@echo "  markdown  - Build Markdown documentation"
	@echo "  readmeio - Generate readme.io docs with frontmatter"
	@echo "  docs      - Build all (markdown, html, and readme.io)"
	@echo "  clean     - Remove build artifacts"

# Clean build directory
clean:
	rm -rf $(BUILDDIR)

# Build HTML documentation
html:
	@$(SPHINXBUILD) -M html "$(SPHINXDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build Markdown documentation
markdown:
	@$(SPHINXBUILD) -M markdown "$(SPHINXDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@echo "Build finished. The Markdown files are in $(BUILDDIR)/markdown."
	@cp $(BUILDDIR)/markdown/*.md $(GIT_ROOT)/docs/
	@echo "Markdown files copied to docs/"

# Generate readme.io documentation with YAML frontmatter
readmeio:
	@$(SPHINXBUILD) -M readmeio "$(SPHINXDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@echo "readme.io docs generated in $(BUILDDIR)/readmeio/"

# Build all documentation
docs: clean markdown html readmeio
