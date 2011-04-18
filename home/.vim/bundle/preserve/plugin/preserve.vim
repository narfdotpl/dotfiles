" http://technotales.wordpress.com/2010/03/31/preserve-a-vim-function-that-keeps-your-state/
function! Preserve(command)
    " save last search and cursor position
    let _s=@/
    let l = line(".")
    let c = col(".")

    " do the business
    execute a:command

    " restore previous search history and cursor position
    let @/=_s
    call cursor(l, c)
endfunction
