require("github-theme").setup({
  options = {
    styles = {
      functions = 'bold',
      comments = 'italic',
      keywords = 'bold',
      types = 'italic,bold',
    }
  },
  palettes = {
    github_light_colorblind = { bg = '#FDF6E3', },
    github_dark_colorblind = { bg1 = '#FDF6E3', bg0 = '#FDF6E3', bg3 = '#FDF6E3' },
  },
  -- options.styles.functions = "italic",
  -- sidebars = {"qf", "vista_kind", "terminal", "packer"},
  --  sidebars = {"terminal"},

  -- Change the "hint" color to the "orange" color, and make the "error" color bright red
  -- colors = {hint = "orange", error = "#ff0000"},

  -- Overwrite the highlight groups
  -- overrides = function(c)
  --   return {
  --     htmlTag = {fg = c.red, bg = "#282c34", sp = c.hint, style = "underline"},
  --     DiagnosticHint = {link = "LspDiagnosticsDefaultHint"},
  --     -- this will remove the highlight groups
  --     TSField = {},
  --   }
  -- end
})
local auto_dark_mode = require('auto-dark-mode')

auto_dark_mode.setup({
  update_interval = 1000,
  set_dark_mode = function()
    vim.api.nvim_set_option_value('background', 'dark', {})
    vim.cmd.colorscheme('github_dark_colorblind')
  end,
  set_light_mode = function()
    vim.api.nvim_set_option_value('background', 'light', {})
    vim.cmd.colorscheme('github_light_colorblind')
  end,
})
