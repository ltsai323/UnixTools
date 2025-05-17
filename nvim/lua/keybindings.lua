vim.g.mapleader = ","
vim.g.maplocalleader = ","

local map = vim.api.nvim_set_keymap
local opt_show = {noremap = true, silent = false }
local opt_hide = {noremap = true, silent = true }

map('v', '<', '<gv', opt_hide)
map('v', '>', '>gv', opt_hide)


map('i', '<F1>', '<ESC>:w<CR>', opt_show) -- execute : write file
-- map('n', '', '@:', opt_show) -- execute last : command
map('n', '<C-=>', '@:', { noremap = true, silent = false })

map('n', '<F1>', ':w<CR>', opt_show) -- execute : write file
map('n', '<F2>', ':tabe<space>', opt_show)

map('n', '<F3>', ':w<CR>:! python3 %', opt_show)
map('n', '<F4>', ':w<CR>:! <Up>', opt_show)

map('n', '<F8>', ':tabp<CR>', opt_show)
map('n', '<F9>', ':tabn<CR>', opt_show)

map('n', '<leader>W', ':call DeleteTrailingWS()<CR>', opt_show)
map('n', '<leader>R', ':call ReloadVIMRC<CR>', opt_show)

map('', '<ScrollWheelUp>', '<Nop>', {noremap = false})
map('', '<S-ScrollWheelUp>', '<Nop>', {noremap = false})
map('', '<C-ScrollWheelUp>', '<Nop>', {noremap = false})
map('', '<ScrollWheelDown>', '<Nop>', {noremap = false})
map('', '<S-ScrollWheelDown>', '<Nop>', {noremap = false})
map('', '<C-ScrollWheelDown>', '<Nop>', {noremap = false})
map('', '<ScrollWheelLeft>', '<Nop>', {noremap = false})
map('', '<S-ScrollWheelLeft>', '<Nop>', {noremap = false})
map('', '<C-ScrollWheelLeft>', '<Nop>', {noremap = false})
map('', '<ScrollWheelRight>', '<Nop>', {noremap = false})
map('', '<S-ScrollWheelRight>', '<Nop>', {noremap = false})
map('', '<C-ScrollWheelRight>', '<Nop>', {noremap = false})




