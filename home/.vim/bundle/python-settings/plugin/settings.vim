" don't special-highlight exceptions
let python_no_exception_highlight = 1

" run flake8 on save
autocmd BufWritePost *.py call Flake8()
