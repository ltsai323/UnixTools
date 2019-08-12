" .vimrc
" See: http://vimdoc.sourceforge.net/htmldoc/options.html for details
" usage : 
"   1. execute command :   git clone https://github.com/gmarik/vundle.git ~/.vim/vundle
"   2. open vim and execute command    ':PlugInstall'
"   3. if you want to clean the packages useless, use ':BundleClean'

""----  Define System Environment ----------------------------------------------
set backupdir=~/.vim/backup
let s:uname = system("uname -s")
let s:hostname = system("echo $HOSTNAME")
let g:vimenv = $HOME.'/local/.vim'

""----  Indention settings  ----------------------------------------------------
set tabstop=4
set softtabstop=4
set shiftwidth=4
set smarttab
set autoindent
set whichwrap=b,s                   " set whichwrap=b,s,<,>,[,]
set expandtab                       " replace all tab with space
let g:indentLine_char = '┆'
set fdm=marker


""----  Search settings  -------------------------------------------------------
set showmatch
set hlsearch
set hls
set noincsearch

""----  Number column settings  ------------------------------------------------
set number
set numberwidth=3


""----  Misc. Settings  --------------------------------------------------------
set showcmd
set showmode
set completeopt=menuone,longest
set complete=.,b,t,i 
set backspace=0                     " do not allow the backspace
set formatoptions=c,q,r,t
set ruler
set cursorline
set background=dark
set mouse=""                        " disable all mouse action.
set noeb
set linebreak
set history=20
set t_Co=256


""----  NERDTree + CtrlP + TagBar  ---------------------------------------------
let g:NERDTreeShowBookmarks=1
let g:NERDTreeChDirMode=2
let g:ctrlp_working_path_mode='rc'
let g:ctrlp_custom_ignore = {
  \ 'dir':  '\v[\/]\.(git|hg|svn)$',
  \ 'file': '\v\.(exe|so|dll|pyc)$',
  \ 'link': 'some_bad_symbolic_links',
  \ }
let g:ctrlp_cache_dir = $HOME.'/.cache/ctrlp'
let g:ctrlp_cmd = 'CtrlPMRU'
let g:ctrlp_max_depth = 10
let g:ctrlp_max_files = 10000

""----  Open on previous position  ---------------------------------------------
"if has("autocmd")
"   au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$")
"            \| exe "normal! g'\"" | endif
"endif

""----  Custom key mapping  ----------------------------------------------------
noremap    <F1>             <nop>
nnoremap <silent> <F5>      : NERDTreeTabsToggle<CR>
nnoremap    <F2>            :tabe<Space>
nnoremap    <F8>            :tabp<CR>
nnoremap    <F9>            :tabn<CR>

" disable all scrolling
noremap <ScrollWheelUp> <nop>
noremap <S-ScrollWheelUp> <nop>
noremap <C-ScrollWheelUp> <nop>
noremap <ScrollWheelDown> <nop>
noremap <S-ScrollWheelDown> <nop>
noremap <C-ScrollWheelDown> <nop>
noremap <ScrollWheelLeft> <nop>
noremap <S-ScrollWheelLeft> <nop>
noremap <C-ScrollWheelLeft> <nop>
noremap <ScrollWheelRight> <nop>
noremap <S-ScrollWheelRight> <nop>
noremap <C-ScrollWheelRight> <nop>


""----  File name auto completion settings  ------------------------------------
set wildmenu
set wildmode=longest,list
set wildignore+=*.a,*.o
set wildignore+=*.bmp,*.gif,*.ico,*.jpg,*.png
set wildignore+=.DS_Store,.git,.hg,.svn
set wildignore+=*~,*.swp,*.tmp


""----  Vundle settings  -------------------------------------------------------
set nocompatible
filetype off
set rtp+=~/.vim/vundle
call vundle#begin()

Plugin 'scrooloose/nerdtree'
Plugin 'godlygeek/tabular'
Plugin 'Yggdroot/indentLine'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'drmingdrmer/vim-syntax-markdown'
Plugin 'octol/vim-cpp-enhanced-highlight'
Plugin 'Mizuchi/STL-Syntax'
Plugin 'hdima/python-syntax'
call vundle#end()
filetype on 
filetype plugin on
filetype indent on 

""----  Molokai settings  ------------------------------------------------------
syntax on
set t_Co=256
colorscheme molokai
let g:molokai_original=1
"let g:rehash256 = 1
hi Normal ctermbg=none 
"private
hi String  ctermfg=11

if filereadable(g:vimenv.'/colors/jellybeans.vim/colors/jellybeans.vim')
    let g:jellybeans_background_color_256="none"
    colo jellybeans
    hi Search cterm=bold,standout ctermfg=11 
    hi Comment cterm=underline ctermfg=243
    hi Error cterm=bold,underline ctermbg=9 ctermfg=228
    exec "hi Folded ctermbg=232".g:jellybeans_background_color_256
    exec "hi CursorLine ctermbg=235".g:jellybeans_background_color_256 

    hi CursorColumn ctermbg=52
    hi PmenuSel cterm=bold ctermfg=9 ctermbg=228
    hi MatchParen cterm=bold ctermfg=none ctermbg=228
    hi SpecialKey ctermfg=9
    if v:version >= 703
        "let &colorcolumn="80,".join(range(160,999,80),",")  " highlight i-th column
        "exec "hi ColorColumn cterm=underline ctermbg=".g:jellybeans_background_color_256
        exec "hi DiffChange ctermbg=1"
    endif
else
    colo default
endif

""----  YouCompleteMe, UltiSnip with super tab ---------------------------------
"let g:ycm_key_list_select_completion = ['<C-n>', '<Down>']
"let g:ycm_key_list_previous_completion = ['<C-p>', '<Up>']
"let g:SuperTabDefaultCompletionType = '<C-n>'
"" better key bindings for UltiSnipsExpandTrigger
"let g:UltiSnipsExpandTrigger = "<tab>"
"let g:UltiSnipsJumpForwardTrigger = "<tab>"
"let g:UltiSnipsJumpBackwardTrigger = "<s-tab>"
"" Disable Tex concealing
"let g:tex_conceal = ""
"" Disable YCM auto complete windows 
"set completeopt-=preview
"let g:ycm_add_preview_to_completeopt = 0 
"" Disable auto syntaz checker 
"let g:ycm_register_as_syntastic_checker = 0


set term=xterm-256color

"""----  Markdown syntax settings  ----------------------------------------------
"let g:vim_markdown_math=1
"let g:vim_markdown_frontmatter=1
"
"function Astyle()
"   exec "%!astyle"
"endfunction

"""----  Syntex for C++, STL and Python  ----------------------------------------
"""C++
let g:cpp_class_scope_highlight = 1
let g:cpp_member_variable_highlight = 1
let g:cpp_class_decl_highlight = 1
"let g:cpp_experimental_simple_template_highlight = 1
let g:cpp_concepts_highlight = 1
"let g:cpp_no_function_highlight = 1
"""Python
let python_highlight_all = 1


"""---- Encoding ----------------------------------------------------------------
set fileformat=unix
set fileformats=unix,mac,dos
set encoding=utf-8
set termencoding=utf-8
set fileencoding=utf-8
set spelllang=en_us

"""---- Assign comment symbols --------------------------------------------------
autocmd FileType vim        let b:comment_leader = '"'
autocmd Filetype vimwiki    let b:comment_leader = '%%'
autocmd FileType make       let b:comment_leader = '#'
autocmd FileType sh         let b:comment_leader = '#'
autocmd FileType python     let b:comment_leader = '#'
autocmd FileType c,cc,cpp   let b:comment_leader = '//'
autocmd FileType java       let b:comment_leader = '//'
autocmd FileType tex        let b:comment_leader = '%'
autocmd Filetype html,xml   let b:comment_leader = '<!--'
autocmd Filetype html,xml   let b:comment_tailer = '-->'
autocmd Filetype markdown   let b:comment_leader = '<!--'
autocmd Filetype markdown   let b:comment_tailer = '-->'
autocmd FileType conf,fstab let b:comment_leader = '#'
