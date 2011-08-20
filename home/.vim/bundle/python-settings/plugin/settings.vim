" don't special-highlight exceptions
let python_no_exception_highlight = 1

" use magic colon
autocmd FileType python :inoremap <buffer> : <Esc>$a:<Esc>o
autocmd FileType python :snoremap <buffer> : <Esc>$a:<Esc>o

" use pyflakes on save
function! Pyflakes()
    silent make
    redraw
    try
        cc
    catch E42
    endtry
endfunction
autocmd BufNewFile,BufRead *.py :compiler pyflakes
autocmd BufWritePost *.py :call Pyflakes()
