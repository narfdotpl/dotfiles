" don't special-highlight exceptions
let python_no_exception_highlight = 1

" use magic colon
autocmd FileType python :inoremap <buffer> : <Esc>$a:<Esc>o
autocmd FileType python :snoremap <buffer> : <Esc>$a:<Esc>o

" run pyflakes on save
autocmd BufNewFile,BufRead *.py :compiler pyflakes
autocmd BufWritePost *.py :silent make | cwindow
