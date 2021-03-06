" check my english
autocmd FileType markdown :set spell
autocmd FileType markdown :set spelllang=en

" write a pair of stars
autocmd FileType markdown :inoremap <buffer> * **<Left>

" underline titles with \= and \-
autocmd FileType markdown :nnoremap \= yypVr=o<Esc>
autocmd FileType markdown :nnoremap \- yypVr-o<Esc>

" wrap nicely
autocmd FileType markdown :set wrap linebreak nolist
