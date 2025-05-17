-- Only required if you have packer configured as `opt`
vim.cmd [[packadd packer.nvim]]
local packer_exists = pcall(vim.cmd, [[packadd packer.nvim]])


vim.g.minimap_auto_start = 1 -- mini map setup
return require('packer').startup(function(use)
  -- Packer can manage itself
  use 'wbthomason/packer.nvim'

  -- Simple plugins can be specified as strings
  use 'rstacruz/vim-closer'


  -- to use ./markmap.lua
  use 'nvim-lua/plenary.nvim'  -- Packer can load this as a utility plugin

  -- Lazy loading:
  -- Load on specific commands
  use {'tpope/vim-dispatch', opt = true, cmd = {'Dispatch', 'Make', 'Focus', 'Start'}}

  -- Load on an autocommand event
  use {'andymass/vim-matchup', event = 'VimEnter'}

  use({ 'projekt0n/github-nvim-theme'})

  use({ 'f-person/auto-dark-mode.nvim'}) -- Auto Dark Mode plugin
  use({ 'wfxr/minimap.vim', run = 'cargo install --locked code-minimap' }) -- mini map at right

  use({ 'sbdchd/neoformat' }) -- Code formatting plugin
end)
