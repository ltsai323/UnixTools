-- Install `npm install -g markmap-cli` for first
-- Lua function to call Markmap on the current file and save to a specific directory
function MarkmapPreview()
  local current_file = vim.fn.expand("%:p")
  local output_dir = "/Users/noises/workspace/MindNotte/MindRecord"  -- Change this to your desired output directory
  local output_file = output_dir .. "/" .. vim.fn.fnamemodify(current_file, ":t:r") .. ".html"  -- Output file with the same base name as the input file

  -- Ensure the output directory exists
  vim.fn.mkdir(output_dir, "p")

  -- Run Markmap and specify the output file
  vim.fn.system(string.format('markmap %s -o %s', current_file, output_file))
  
  print("Opening mindmap for " .. current_file .. " at " .. output_file)
end

-- Create a Neovim command for MarkmapPreview
vim.api.nvim_create_user_command('MarkmapPreview', function()
  MarkmapPreview()
end, {})

-- Optional: Add custom Markmap keybinding
-- vim.api.nvim_set_keymap('n', '<leader>mm', ':MarkmapPreview<CR>', { noremap = true, silent = true })
