" vim: set ft=vim fdm=marker:
" Last Modified   : 12 Feb 2017 18:40 2016

" Update
" wget -O ~/lxHome/scripts/setEnv/vimrc https://www.dropbox.com/s/fpu3oqzvi8x1mkq/vimrc?dl=0
" See :help option
"     :set all
"     /usr/share/vim/vim74/vimrc_example.vim
"     https://github.com/yangyangwithgnu/use_vim_as_ide/blob/master/README.md



" Define system environment
set	backupdir=~/.vim/backup
let s:uname = system("uname -s")
let s:hostname = system("echo $HOSTNAME")
let g:vimenv = $HOME.'/local/.vim'

" Basic vim settings and initialize plugin-manager {{{
" Install/Update plugins by :PluginInstall :PluginUpdate
if !filereadable($HOME.'/.vim/autoload/plug.vim')
    echo "Installing vim-plug...\n"
    silent !mkdir -p ~/.vim/autoload
    silent !wget --no-check-certificate -O ~/.vim/autoload/plug.vim https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif
set nocompatible
filetype off
""""""" If there is error on PluginStall
""""""""""" There are two known solutions:
""""""""""" 1. Check if there is ~/local/.vim/
""""""""""" 2. Check if there is "wget" command in your system
""""""""""" 3. Check if there is "git" command in your system

""" if you saw errors at the function, make sure you owns the directory: $HOME/local/.vim
call plug#begin(g:vimenv.'/bundle') 
    " The lookings, get powerline-fonts from yum/apt.
Plug 'Yggdroot/indentLine'
Plug 'nanotech/jellybeans.vim', {'dir': g:vimenv.'/colors/jellybeans.vim'}
Plug 'junegunn/goyo.vim'
"Plug 'junegunn/limelight.vim'
    " Better way to browse files
Plug 'vim-scripts/LargeFile'
Plug 'scrooloose/nerdtree'
Plug 'jistr/vim-nerdtree-tabs'
let s:loaded_youcompleteme=1
if filereadable(g:vimenv.'/bundle/YouCompleteMeOblitum/README.md')
    Plug 'https://github.com/oblitum/YouCompleteMe', { 'do': g:vimenv.'/bundle/YouCompleteMe/install.sh --clang-completer', 'dir': g:vimenv.'/bundle/YouCompleteMeOblitum', 'frozen': 1}
    Plug 'SirVer/ultisnips'
    Plug 'honza/vim-snippets'
elseif filereadable(g:vimenv.'/bundle/YouCompleteMe/README.md')
    Plug 'https://github.com/Valloric/YouCompleteMe', { 'do': g:vimenv.'/bundle/YouCompleteMe/install.sh --clang-completer', 'dir': g:vimenv.'/bundle/YouCompleteMe', 'frozen': 1}
    Plug 'SirVer/ultisnips' " Some error in lxplus?
    Plug 'honza/vim-snippets'
else
    let s:loaded_youcompleteme=0
    Plug 'vim-scripts/L9'
    Plug 'othree/vim-autocomplpop'
endif
    " Syntax check/highlight
Plug 'scrooloose/syntastic' ", {'on': 'SyntasticCheck'}
"Plug 'valloric/MatchTagAlways'
Plug 'octol/vim-cpp-enhanced-highlight', {'dir': g:vimenv.'/syntax/vim-cpp-enhanced-highlight'}
Plug 'Mizuchi/STL-Syntax', {'dir': g:vimenv.'syntax/STL-Syntax'}
Plug 'hdima/python-syntax', {'dir': g:vimenv.'/syntax/python-syntax'}
"Plug 'othree/html5.vim', {'dir': g:vimenv.'/syntax/html5.vim'}
"Plug 'jelera/vim-javascript-syntax', {'dir': g:vimenv.'/syntax/vim-javascript-syntax'}
call plug#end()
filetype plugin indent on "}}}

" Vim settings
let g:LargeFile = 20
set mouse=""                        " disable all mouse action.
set modeline
set modelines=5                     " OSX set default value to 0
set history=20                      " keep N lines of command line history
set viminfo='20,\"50,:20,%          " read/write a .viminfo file.
set ttyfast
"set visualbell
set showcmd
set showmode
set wildmenu
set wildmode=longest,list
set wildignore+=*.o,*.a,*.so,*.obj,*.exe,*.lib,*.pyc
set wildignore+=*.png,*.jpg,*.gif,*.pdf
"set wildignore+=*.root
set completeopt=menuone,longest
set complete=.,b,t,i " see :h cpt
autocmd FileType python          setlocal omnifunc=pythoncomplete#Complete
autocmd FileType javascript      setlocal omnifunc=javascriptcomplete#CompleteJS
autocmd FileType css             setlocal omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown   setlocal omnifunc=htmlcomplete#CompleteTags
autocmd FileType xml             setlocal omnifunc=xmlcomplete#CompleteTags
"set laststatus=2
"set statusline=%<%f\ %h%m%r%=%-14.(%l,%c%V%)\ %P
"set ignorecase
"set smartcase
set noincsearch
set showmatch
autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif " Jump to last known position

" Encoding
set fileformat=unix
set fileformats=unix,mac,dos
set encoding=utf-8
set termencoding=utf-8
set fileencodings=ucs-bom,utf-8,euc-jp,big5,cp936,gb18030,latin1
set fileencoding=utf-8
set spelllang=en_us

" Typesettings
set autoindent
set backspace=0                     " do not allow the backspace
set whichwrap=b,s                   " set whichwrap=b,s,<,>,[,]
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab                       " replace all tab with space
"set list listchars=tab:\|\-,conceal:\ ,trail:-
set fdm=marker                      " syntax/text
"set foldlevel=1
set wrap
set linebreak
set noeb


" ColorScheme setting, check schemes by :colo <TAB>
" Check current highlight by :highlight
"syntax enable

"   use 256 color
set t_Co=256
set hls                             " highlight search result
set ruler                           " show the cursor position all the time
set cursorline                      " add an underline under the cursor
set number
set numberwidth=3                   " width of line-number
if filereadable(g:vimenv.'/colors/jellybeans.vim/colors/jellybeans.vim')
    let g:jellybeans_background_color_256="none"
    colo jellybeans
    hi Search cterm=bold,standout ctermfg=11 
    hi Comment cterm=underline ctermfg=243
    hi Error cterm=bold,underline ctermbg=9 ctermfg=228
    exec "hi Folded ctermbg=232".g:jellybeans_background_color_256
    "darkBG
    "exec "hi CursorLine ctermbg=233".g:jellybeans_background_color_256 
    "modified solarized
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
"hi Cursor cterm=standout,bold
    " Other highligh stuff
    "
function! MyPlaceholderHighlight() abort "{{{
  highlight abridgePlaceholder ctermfg=9 ctermbg=228
endfunction "}}}
autocmd VimEnter,ColorScheme * call MyPlaceholderHighlight()

" Filetype settings
autocmd BufNewFile,BufReadPost *.md set filetype=markdown
    " c and cpp settings
let g:cpp_class_scope_highlight = 1
    " python settings
let python_highlight_all=1
let b:python_version_2=1
    " latex settings
let g:tex_flavor = "latex"
let g:tex_conceal="bdmg" " abdmgs
let g:tex_fast="bcmMprsSvV" "bcmMprsSvV
let g:tex_no_error = 1
autocmd Filetype make       setlocal noet
autocmd Filetype c,cc,cpp   setlocal equalprg=indent\ -kr\ -l120\ -cli4\ -nut\ -bbo
autocmd Filetype perl       setlocal equalprg=perltidy
autocmd Filetype tex        setlocal spell|setlocal conceallevel=0
autocmd Filetype markdown   setlocal spell

    " Quick compile settings, run compile by :make or <F9> in normal mode
nnoremap <F9> <ESC>:make!<CR>
if !filereadable(expand("%:p:h")."/Makefile")
    autocmd Filetype cc,c,cpp   setlocal makeprg=g++\ -Werror\ -o\ %<\ %\ &&\ ./%:r
    autocmd Filetype vimwiki    nnoremap <buffer> <F9> <ESC>:Vimwiki2HTMLBrowse<CR>
endif

" Plugin settings
let mapleader=","


    " Limelight+Goyo"{{{
let g:goyo_width = 100
let g:goyo_height = 85
let g:goyo_linenr = 2

function! s:goyo_enter()
    let &scrolloff=999-&scrolloff
    Limelight
endfunction

function! s:goyo_leave()
    let &scrolloff=999-&scrolloff
    hi Search cterm=bold,standout
    Limelight!
endfunction

autocmd! User GoyoEnter nested call <SID>goyo_enter()
autocmd! User GoyoLeave nested call <SID>goyo_leave()

let g:limelight_conceal_ctermfg = 'gray'
let g:limelight_conceal_ctermfg = 240
let g:limelight_default_coefficient = 0.5
let g:limilight_priority = -1

"autocmd VimEnter,ColorScheme * :Limelight

"}}}

    " NerdTree+CtrlP+Tagbar "{{{
let g:NERDTreeShowBookmarks=1
let g:NERDTreeChDirMode=2 " let ctrlP perform search under selected path
nnoremap <silent> <F5> : NERDTreeTabsToggle<CR>
"autocmd StdinReadPre * let s:std_in=1
"autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
let g:ctrlp_working_path_mode = 'rc'
let g:ctrlp_open_new_file = 't'
let g:ctrlp_custom_ignore = {
  \ 'dir':  '\v[\/]\.(git|hg|svn)$',
  \ 'file': '\v\.(exe|so|dll|pyc)$',
  \ 'link': 'some_bad_symbolic_links',
  \ }
let g:ctrlp_cache_dir = $HOME.'/.cache/ctrlp'
let g:ctrlp_cmd = 'CtrlPMRU'
let g:ctrlp_max_depth = 10
let g:ctrlp_max_files = 10000
if executable('ag')
    set grepprg=ag\ --nogroup\ --nocolor\ --hidden
    let g:ctrlp_user_command = 'ag %s -l --nocolor --nogroup --hidden -i -g ""'
else
    let g:ctrlp_user_command = 'find %s -type f'
endif
let g:ctrlp_match_func = { 'match': 'pymatcher#PyMatch' }
let g:ctrlp_lazy_update = 350
let tagbar_width=50
let g:tagbar_compact=1
"}}}

    " Syntax, jump between errors by :lnext :lprev "{{{
let g:syntastic_mode_map = { "mode": "passive",
                           \ "active_filetypes": ['javascript', 'tcl' , 'markdown'],
                           \ "passive_filetypes": ['sh', 'c' , 'cc', 'cpp', 'python', 'tex'] }
let g:syntastic_auto_loc_list = 1
let g:syntastic_loc_list_height = 5
"let g:syntastic_auto_jump = 1
let g:syntastic_aggregate_errors = 1
if system("which root-config") != ""
    let g:syntastic_cpp_compiler_options = substitute(system("root-config --incdir"),'\(^.*\)\n$','-Werror -I\1','')
    let g:syntastic_c_compiler_options = substitute(system("root-config --incdir"),'\(^.*\)\n$','-Werror -I\1','')
endif
let g:syntastic_python_checkers = ['pylint', 'python']
let g:syntastic_python_pylint_args = "-disable=C0301,C0103,R0914,R0903"
    " vim-surround
let g:surround_insert_tail = "<++>"
"}}}


    " Rearrange annoying default key-bindings
noremap    <F1>        <nop>
nnoremap <silent> <F5> : NERDTreeTabsToggle<CR>
nnoremap    <F2>        :tabe<Space>
"nnoremap  <C-F4>        :tabe<Space>
nnoremap    <F8>        :tabp<CR>
nnoremap    <F9>        :tabn<CR>
inoremap <F10> <ESC>:SyntasticCheck<CR>
nnoremap <F12> <ESC>:Goyo<CR>
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
    " Easy-Commenter ,<C-B> back to home, <C-E> jump to end. "{{{
let b:comment_leader = ''
let b:comment_tailer = ''
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
let g:NERDCustomDelimiters = {
    \ 'c'   : { 'leftAlt': '/*','rightAlt': '*/', 'left': '//', 'right': '' },
    \ 'cc'  : { 'leftAlt': '/*','rightAlt': '*/', 'left': '//', 'right': '' },
    \ 'cpp' : { 'leftAlt': '/*','rightAlt': '*/', 'left': '//', 'right': '' },
    \ 'rst' : { 'leftAlt': ''  ,'rightAlt': ''  , 'left':'.. ', 'right': '' },
\ }
"}}}
    " templates, headers, and timestamps
"execute pathogen#infect('bundle/{}','~/.vim/bundle/{}')
let g:indentLine_char = '┆'

" List of registered cmd, functions, hotkyes. Consult :map and :imap
" Mode index=[f:function, i:insert, n:normal, v:visual x:visual+select]
" i     <C-l>                           : i:Simple placehloder
" i     <C-[jk]>                        : i:Ultisnip
" n     f[swbjf/]                       : n:Easymotion fast jumping
" n     <F2>                            : n:new tab
" n     <F5>                            : n:nerdtree
" n     <F8>                            : n:previous tab
" n     <F9>                            : n:next tab
" n     <F10>                           : n:make / i:SyntasticCheck
" n     <F12>                           : n:Goyo

