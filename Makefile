all: fix build ## (default) the primary pipeline. Will fix anything fixable and then build the result.

help:  ## Display this help
# Taken from https://gist.github.com/prwhite/8168133
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: run
.PHONY: build
.PHONY: spell
.PHONY: spell-fix
.PHONY: fix


run: ## Run Zensical locally
	uv run zensical serve
build: ## Build the static bundle with Zensical
	uv run zensical build
spell: ## Run spellchecker (readonly)
	uv run typos
spell-fix: ## Run spellchecker and fix issues
	uv run typos -w
fix: spell-fix ## Run any fixes

