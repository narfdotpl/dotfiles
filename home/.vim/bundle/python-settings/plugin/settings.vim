" don't special-highlight exceptions
let python_no_exception_highlight = 1

" run pyflakes on save
autocmd BufNewFile,BufRead *.py :compiler pyflakes
autocmd BufWritePost *.py :silent make | cwindow
