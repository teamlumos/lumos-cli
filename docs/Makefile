# Makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= uv run sphinx-build
SPHINXDIR     = sphinx
BUILDDIR      = $(SPHINXDIR)/_build

.PHONY: help clean html markdown docs

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Available targets:"
	@echo "  html      - Build HTML documentation"
	@echo "  markdown  - Build Markdown documentation"
	@echo "  docs      - Build both"
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

# Build both
docs: markdown html
