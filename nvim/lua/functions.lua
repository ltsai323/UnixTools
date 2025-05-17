vim.cmd([[
function! DeleteTrailingWS()
    " Move to the start of the line
    execute "normal! mz"
    " Substitute trailing whitespace with nothing and apply to the whole buffer
    execute '%s/\s\+$//ge'
    " Move back to the cursor position
    execute "normal! `z"
endfunction
]])

