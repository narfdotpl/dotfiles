" fontsized.vim
" =============
"
" Vim magic that handles font sizes, window widths, window movement, etc.
" This is a personal spaghetti-kind-of-hack, not a general purpose plugin.
"
" Four true/false state variables are used:
"  - wide -- are two vertical windows used or just one?
"  - fullscreen -- do you want to use the whole screen?
"
" Maciej Konieczny <hello@narf.pl>
" https://github.com/narfdotpl/dotfiles


" set defaults
let g:fontsized_fullscreen = 0
let g:fontsized_wide = 0


" show four-character-long line numbers
windo set number numberwidth=4

" show status line only if there are at least two windows
set laststatus=1

" show cursor position
set ruler

" show tabs
set showtabline=1

" make vertical split line 'invisible'
set fillchars=
highlight! link VertSplit NonText

" remove ugly yellow line number highlight
highlight! link CursorLineNr LineNr

" set font size
set macligatures
set guifont=FiraCode-Retina:h20


function! s:Fontsized()
    " set width
    if g:fontsized_wide
        set columns=167
    else
        set columns=83
    endif

    " set height
    if g:fontsized_fullscreen
        set fuoptions=background:Normal,maxvert
    else
        set lines=666
    endif

    " restart fullscreen to get maximal window height (needed when changing
    " font size)
    set nofullscreen
    if g:fontsized_fullscreen
        set fullscreen
    endif

    " balance window sizes
    execute "normal \<C-W>="
endfunction


" activate
call s:Fontsized()


" expose command
command! -nargs=0 Fontsized call s:Fontsized()


" map keys:
"  -  change window size with alt + ctrl + arrow
"  -  toggle focus with alt + ctrl + enter
map <A-C-Up> :let g:fontsized_fullscreen = 1<Enter>
            \:Fontsized<Enter>
map <A-C-Right> :let g:fontsized_wide = 1<Enter>
               \:Fontsized<Enter>
map <A-C-Down> :let g:fontsized_fullscreen = 0<Enter>
              \:Fontsized<Enter>
map <A-C-Left> :let g:fontsized_wide = 0<Enter>
              \:Fontsized<Enter>
map <A-C-Enter> :Goyo<Enter>

imap <A-C-Up> <Esc><A-C-Up>i
imap <A-C-Right> <Esc><A-C-Right>i
imap <A-C-Down> <Esc><A-C-Down>i
imap <A-C-Left> <Esc><A-C-Left>i
imap <A-C-Enter> <Esc><A-C-Enter>i
