.PHONY: help

neovim_backup: ## backup neovim rc file
	sh repo_func.sh ~/.config/nvim/ nvim/
neovim_restore: ## backup neovim rc file
	sh repo_func.sh nvim/ ~/.config/nvim/
vim_backup: ## backup vimrc file
	sh repo_func.sh ~/.vimrc vimrc
vim_restore: ## backup vimrc file
	sh repo_func.sh vimrc ~/.vimrc

bashrc_backup: ## backup bashrc
	sh repo_func.sh ~/.bash_profile     bash_profile
	sh repo_func.sh ~/.bashfunctions.sh bashfunctions.sh
	sh repo_func.sh ~/.bashrc           bashrc
	sh repo_func.sh ~/.bashalias.sh     bashalias.sh
	sh repo_func.sh ~/.bash_sessions    bash_sessions
	sh repo_func.sh ~/.bash_history     bash_history
	sh repo_func.sh ~/.bashvariables.sh bashvariables.sh
bashrc_restore: ## restore bashrc
	sh repo_func.sh bash_profile     ~/.bash_profile
	sh repo_func.sh bashfunctions.sh ~/.bashfunctions.sh
	sh repo_func.sh bashrc           ~/.bashrc
	sh repo_func.sh bashalias.sh     ~/.bashalias.sh
	sh repo_func.sh bash_sessions    ~/.bash_sessions
	sh repo_func.sh bash_history     ~/.bash_history
	sh repo_func.sh bashvariables.sh ~/.bashvariables.sh

inputrc_backup: ## backup inputrc
	sh repo_func.sh  ~/.inputrc inputrc
inputrc_restore: ## restore inputrc
	sh repo_func.sh inputrc     ~/.inputrc

$(BACKUP_DIR):
	$(call check_defined, jobname)
	@echo Folder not found: Initialize folder $(BACKUP_DIR)
	mkdir -p $@

IN_ARGS = [opts]

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} /^[0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

