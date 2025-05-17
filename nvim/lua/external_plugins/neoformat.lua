-- call packer#begin('~/.local/share/nvim/site/pack/packer/start/')
-- 
-- -- Code formatting plugin
-- Plug 'sbdchd/neoformat'
-- 
-- call packer#end()


-- Initialize neoformat options
vim.g.neoformat_enabled_cpp = {'clangformat'}
vim.g.neoformat_enabled_python = {'yapf'}
vim.g.neoformat_enabled_bash = {'shfmt'}
vim.g.neoformat_enabled_javascript = {'prettier'}
-- vim.g.neoformat_enabled_html = {'htmlbeautifier'}
vim.g.neoformat_enabled_html = {'prettier'}
-- vim.g.neoformat_enabled_html = {'js-beautify'}
vim.g.neoformat_enabled_css = {'cssbeautify'}
vim.g.neoformat_enabled_yaml = {'yamlfix'}
vim.g.neoformat_enabled_json = {'jq'}
vim.g.neoformat_enabled_csv = {'csvformat'}

-- Map <leader>f to format the current buffer
vim.api.nvim_set_keymap('n', '<leader>f', ':Neoformat<CR>', { noremap = true, silent = true })
