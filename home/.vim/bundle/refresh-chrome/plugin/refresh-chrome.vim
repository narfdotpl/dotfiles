" Refresh Chrome
" ==============
"
" Vim plugin that refreshes current tab of Google Chrome, either
" manually with `:RefreshChrome` or automatically on buffer save, if
" `let g:refresh_chrome_on_save = 1` command was run.


" set defaults
let g:refresh_chrome_on_save = 0

" refresh chrome
function! s:RefreshChrome()
    call system("osascript -e 'tell application \"Google Chrome\" to tell the active tab of its first window to reload'")
endfunction

" expose command
command! -nargs=0 RefreshChrome call s:RefreshChrome()

" refresh on save
function! s:RefreshChromeOnSave()
    if g:refresh_chrome_on_save
        call s:RefreshChrome()
    endif
endfunction

" use autocmd
autocmd BufWritePost * call s:RefreshChromeOnSave()

" toggle g:refresh_chrome_on_save
nmap <Leader>c :let g:refresh_chrome_on_save = !g:refresh_chrome_on_save<Enter>
