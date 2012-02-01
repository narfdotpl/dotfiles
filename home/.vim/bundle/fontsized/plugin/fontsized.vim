" fontsized.vim
" =============
"
" Vim magic that handles font sizes, window widths, window movement, etc.
" This is a personal spaghetti-kind-of-hack, not a general purpose plugin.
"
" Four true/false state variables are used:
"  - external -- is external display connected?
"  - wide -- are two vertical windows used or just one?
"  - fullscreen -- do you want to use the whole screen?
"  - focused -- do you want to hide clutter?
"
" Maciej Konieczny <hello@narf.pl>
" https://github.com/narfdotpl/dotfiles


" set defaults
let g:fontsized_focused = 0
let g:fontsized_fullscreen = 0
let g:fontsized_wide = 0


function! s:Fontsized()
    " detect external display
    if system("ioreg -rc AppleDisplay") == ""
        let g:fontsized_external = 0
    else
        let g:fontsized_external = 1
    endif

    " handle 'focused mode' settings
    " TODO: don't use hardcoded colors of dark solarized colorscheme
    if g:fontsized_focused
        " hide things
        highlight NonText guifg=bg
        highlight VertSplit guibg=#002b36
        set fillchars=
        windo set nonumber
        set showtabline=0 laststatus=0 noruler
        let g:fontsized_fullscreen = 1
    else
        " restore colors
        " TODO: as above
        highlight NonText term=bold ctermfg=9 gui=bold guifg=#073642
        highlight VertSplit cterm=reverse guifg=#657b83 guibg=#657b83

        " show four-character-long line numbers
        windo set number numberwidth=4

        " show status line only if there are at least two windows
        set laststatus=1

        " show cursor position
        set ruler

        " show tabs
        set showtabline=1
    endif

    " set actual font sizes and stuff...

    if g:fontsized_external
        set guifont=Monaco:h18
    else
        if g:fontsized_wide
            if g:fontsized_focused
                set guifont=Monaco:h15
            else
                set guifont=Monaco:h14
            endif
        else
            if g:fontsized_fullscreen
                set guifont=Monaco:h18
            else
                set guifont=Monaco:h16
            endif
        endif
    endif

    if g:fontsized_wide
        if g:fontsized_focused
            set columns=159
        else
            set columns=167  " + 2 x 4
        endif

        " balance window sizes
        execute "normal \<C-W>="
    else
        if g:fontsized_focused
            set columns=79
        else
            set columns=83  " + 4
        endif
    endif

    " restart fullscreen to get maximal window height (needed when changing
    " font size)
    set nofullscreen
    if g:fontsized_fullscreen
        if g:fontsized_focused
            set fuoptions=maxvert,background:Normal
        else
            set fuoptions=maxvert
        endif

        set fullscreen
    else
        if !g:fontsized_external && g:fontsized_wide
            set lines=45
        else
            set lines=40
        endif
    endif
endfunction


" activate
call s:Fontsized()


" expose command
command! -nargs=0 Fontsized call s:Fontsized()


" map keys:
"  -  change window size with alt + ctrl + arrow
"  -  focus with alt + ctrl + enter
map <A-C-Up> :let g:fontsized_focused = 0<Enter>
            \:let g:fontsized_fullscreen = 1<Enter>
            \:Fontsized<Enter>
map <A-C-Right> :let g:fontsized_wide = 1<Enter>
               \:Fontsized<Enter>
map <A-C-Down> :let g:fontsized_focused = 0<Enter>
              \:let g:fontsized_fullscreen = 0<Enter>
              \:Fontsized<Enter>
map <A-C-Left> :let g:fontsized_wide = 0<Enter>
              \:Fontsized<Enter>
map <A-C-Enter> :let g:fontsized_focused = 1<Enter>
               \:Fontsized<Enter>
imap <A-C-Up> <Esc><A-C-Up>i
imap <A-C-Right> <Esc><A-C-Right>i
imap <A-C-Down> <Esc><A-C-Down>i
imap <A-C-Left> <Esc><A-C-Left>i
imap <A-C-Enter> <Esc><A-C-Enter>i