-- Automatically install packer
local install_path = vim.fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
if vim.fn.empty(vim.fn.glob(install_path)) > 0 then
  vim.fn.execute('!git clone https://github.com/wbthomason/packer.nvim ' .. install_path)
end

vim.cmd [[packadd packer.nvim]]

require('packer').startup(function(use)
  -- Specify your plugins here
  use 'wbthomason/packer.nvim' -- Packer can manage itself

  -- Example: Install 'nvim-treesitter'
  use {
    'nvim-treesitter/nvim-treesitter',
    run = ':TSUpdate'
  }

  -- Add other plugins below
end)


require('functions')
require('keybindings')
require('basic')
require('external_plugins/init_plugins')
require('external_plugins/colorschemes')
require('external_plugins/markmap')
require('external_plugins/neoformat')

