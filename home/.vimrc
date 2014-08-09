" .vimrc -- Vim configuration file
"
" Maciej Konieczny <hello@narf.pl>
" https://github.com/narfdotpl/dotfiles


"----------
"  basics
"----------

" drop vi compatibility
set nocompatible

" use utf8
set encoding=utf8

" load plugins
call pathogen#infect()
filetype plugin indent on

" move Leader closer to home row
let mapleader=','

" use long history
set history=1000


"--------
"  look
"--------

" show file path in title bar
set title
set titlestring=%F

" simplify gui
if has("gui_running")
    set guioptions-=T  " hide toolbar
    set guioptions-=r  " hide right scrollbar
    set guioptions-=L  " hide left scrollbar in a vertically split window
endif

" display incomplete commands
set showcmd

" autocomplete commands using nice menu in place of window status
set wildmenu

" highlight syntax
syntax on
autocmd BufEnter * :syntax sync fromstart

" highlight current line
set cursorline

" disable cursor blinking in normal mode
set guicursor=n:blinkon0

" disable redraw while executing macros, etc.
set lazyredraw

" show matching brackets
set showmatch

" fight for your eyes
set background=dark
let g:solarized_visibility='low'
let g:solarized_italic=0
colorscheme solarized

" switch between sides of the force
map <Leader><F1> :set background=dark<Enter>:Fontsized<Enter>
map <Leader><F2> :set background=light<Enter>:Fontsized<Enter>


"--------------
"  whitespace
"--------------

" show tabs
set list
set listchars=tab:▸\ ,

" use four spaces instead of tabs
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab   " convert tabs to spaces
set autoindent  " use automagic indentation

" round indent to multiple of 'shiftwidth'
set shiftround

" temporarily change tab size
nnoremap <Leader><Tab>2 :setlocal ts=2 sts=2 sw=2 et<Enter>
nnoremap <Leader><Tab>4 :setlocal ts=4 sts=4 sw=4 et<Enter>
nnoremap <Leader><Tab><Tab> :setlocal ts=4 sts=4 sw=4 noet<Enter>

" indent with cmd + [/]
nnoremap <D-[> <<
imap <D-[> <Esc><D-[>i
vnoremap <D-[> <gv
nnoremap <D-]> >>
imap <D-]> <Esc><D-]>i
vnoremap <D-]> >gv

" remove trailing whitespace on save
autocmd BufWritePre * :call Preserve('%s/\s\+$//e')


"--------------
"  completion
"--------------

set completeopt=longest,menu

" take advantage of TextMate muscle memory
inoremap <F1> <C-p>
nmap <F1> a<F1>


"----------
"  search
"----------

" highlight matches
set hlsearch   " highlight
set incsearch  " highlight as you type

" ignore case when searching
set ignorecase  " ignore
set smartcase   " don't ignore if pattern contains upper case characters

" turn off highlighting with F2
nnoremap <F2> :nohlsearch<Enter>
imap <F2> <Esc><F2>a
vmap <F2> <Esc><F2>gv
smap <F2> <C-g><F2><C-g>

" replace last search
nnoremap <Leader>s :%s///gc<Left><Left><Left>
vnoremap <Leader>s :s///gc<Left><Left><Left>


"-----------
"  windows
"-----------

" open new windows right and below
set splitright
set splitbelow

" move between windows with alt + cmd + arrow
nnoremap <A-D-up> <C-w><C-k>
nnoremap <A-D-right> <C-w><C-l>
nnoremap <A-D-left> <C-w><C-h>
nnoremap <A-D-down> <C-w><C-j>
imap <A-D-up> <Esc><A-D-up>i
imap <A-D-right> <Esc><A-D-right>i
imap <A-D-left> <Esc><A-D-left>i
imap <A-D-down> <Esc><A-D-down>i

" swap windows
map <Leader>x <C-w><C-x>

" balance windows size
map <Leader>= <C-w><C-=>


"--------
"  tabs
"--------

" limit number of open tabs to 50
set tabpagemax=50


"------------
"  movement
"------------

" disable mvim modifier movements
if has("gui_macvim")
    let macvim_skip_cmd_opt_movement = 1
endif

" allow backspacing over everything
set backspace=indent,eol,start

" use screen lines when using arrows
nnoremap <Up> gk
nnoremap <Down> gj
imap <Up> <Esc><Up>a
imap <Down> <Esc><Down>a

" keep a few screen lines around the cursor
set scrolloff=3

" make big jumps with cmd + arrow
nnoremap <D-Up> gg
nnoremap <D-Right> g$
nnoremap <D-Down> G
nnoremap <D-Left> g0
imap <D-Up> <Esc><D-Up>i
imap <D-Right> <Esc><D-Right>a
imap <D-Down> <Esc><D-Down>i
imap <D-Left> <Esc><D-Left>i

" jump between words with with alt + arrow
nnoremap <A-Right> e
nnoremap <A-Left> b
imap <A-Right> <Esc><A-Right>a
imap <A-Left> <Esc><A-Left>i

" delete beginning of a word with alt + bs
inoremap <A-BS> <C-W>

" delete beginning of a line with cmd + bs
inoremap <D-BS> <Esc>d0xi

" use cmd + enter like in TextMate
nnoremap <D-Enter> o
imap <D-Enter> <Esc><D-Enter>
smap <D-Enter> <Esc><D-Enter>

" move current line/selection with alt + up/down
nnoremap <A-Up> :m-2<Enter>
nnoremap <A-Down> :m+1<Enter>
imap <A-Up> <Esc><A-Up>i
imap <A-Down> <Esc><A-Down>i
vnoremap <A-Up> :m'<-2<Enter>gv
vnoremap <A-Down> :m'>+1<Enter>gv
smap <A-Up> <C-g><A-Up><C-g>
smap <A-Down> <C-g><A-Down><C-g>


"-------------
"  selecting
"-------------

" use shift or mouse to select
set selectmode=mouse,key
set keymodel=startsel,stopsel

" escape selection and enter insert mode
snoremap <Up> <Esc>ki
snoremap <Right> <Esc>`>a
snoremap <Down> <Esc>ji
snoremap <Left> <Esc>`<i

" exchange cursor position
snoremap <F1> <C-G>o<C-G>

" shift + arrow
inoremap <S-Up> <Esc>vkl<C-G>
inoremap <S-Right> <Esc>lv<C-G>
inoremap <S-Down> <Esc>vj<C-G>
inoremap <S-Left> <Esc>v<C-G>

" alt + shift + arrow
imap <A-S-Right> <Right><Esc><A-S-Right>
nnoremap <A-S-Right> ve<C-G>
snoremap <A-S-Right> <C-G>e<C-G>
imap <A-S-Left> <Esc><A-S-Left>
nnoremap <A-S-Left> vb<C-G>
snoremap <A-S-Left> <C-G>b<C-G>

" cmd + shift + arrow
imap <D-S-Up> <Esc><D-S-Up>
nnoremap <D-S-Up> v0gg<C-G>
snoremap <D-S-Up> <C-G>0gg<C-G>
imap <D-S-Right> <Right><Esc><D-S-Right>
nnoremap <D-S-Right> v$h<C-G>
snoremap <D-S-Right> <C-G>$h<C-G>
imap <D-S-Down> <Esc>l<D-S-Down>
nnoremap <D-S-Down> v0G<C-G>
snoremap <D-S-Down> <C-G>0G<C-G>
imap <D-S-Left> <Esc><D-S-Left>
nnoremap <D-S-Left> v0<C-G>
snoremap <D-S-Left> <C-G>0<C-G>


"------------------
"  other mappings
"------------------

" delete current line
nnoremap <bs> dd

" join upwards
nnoremap K kJ

" change selection/word to lowercase and restore mode
vnoremap <C-L> uv`]
imap <C-L> <Esc><C-L>a
nmap <C-L> viw<C-L><Esc>
smap <C-L> <C-G><C-L><C-G>

" change selection/word to uppercase and restore mode
vnoremap <C-U> Uv`]
imap <C-U> <Esc><C-U>a
nmap <C-U> viw<C-U><Esc>
smap <C-U> <C-G><C-U><C-G>

" change line to titlecase and restore mode
nnoremap <C-T> V:!title<Enter>$
imap <C-T> <Esc><C-T>a

" insert colon at the end of a line
inoremap <S-Enter> <Esc>:call Preserve('s/\s*$/;/')<Enter>a

" make braced block
inoremap <A-Enter> <Space>{}<Left><Enter><Esc>O

" open tag definition in a new tab
nnoremap <D-\> :tab split<Enter>:exec("tag ".expand("<cword>"))<Enter>

" switch between normal and relative line numbers
nnoremap <Leader>n :set number<Enter>
nnoremap <Leader>r :set relativenumber<Enter>

" use spell checking
nnoremap <silent> <Leader>:e :set spell<Enter>:set spelllang=en<Enter>
nnoremap <silent> <Leader>:p :set spell<Enter>:set spelllang=pl<Enter>
nnoremap <silent> <Leader>:: :set spell!<Enter>

" change filetype
map <Leader>co :set ft=coffee<Enter>
map <Leader>js :set ft=javascript<Enter>
map <Leader>py :set ft=python<Enter>


"--------
"  else
"--------

" ignore '.DS_Store', '*.pyc' and '*.pyo' files in directory listings
let g:netrw_list_hide='\v(\.DS_Store)|(.*\.py[co])|(\.swp)$'

" learn to type
ab addded added
ab aded added
ab alais alias
ab anythong anything
ab everythong everything

" map alt + colon to colon (my keyboard... don't ask)
inoremap Ú :
