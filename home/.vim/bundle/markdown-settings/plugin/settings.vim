" check my english
autocmd FileType markdown :set spell
autocmd FileType markdown :set spelllang=en

" write a pair of stars
autocmd FileType markdown :inoremap <buffer> * **<Left>

" create a horizontal line and underline titles with \=
autocmd FileType markdown :nnoremap \= yy2PVr-2jVr=o<Esc>o

" underline secondary titles with \-
autocmd FileType markdown :nnoremap \- yypVr-o<Esc>
