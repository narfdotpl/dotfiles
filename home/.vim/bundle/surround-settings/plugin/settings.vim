" write pairs
inoremap ( ()<Left>
inoremap [ []<Left>
inoremap { {}<Left>
inoremap <expr> " <SID>WritePair('""')
inoremap <expr> ' <SID>WritePair("''")
inoremap <expr> ` <SID>WritePair('``')
function! s:WritePair(pair)
    " write only second character of a pair if preceding character is part
    " of a word or equals to first character of this very pair
    let x = col('.') - 1
    let chr = getline('.')[x - 1]
    if x <= 0 || (chr != a:pair[0] && !empty(matchstr(chr, '\W')))
        return a:pair."\<Left>"
    else
        return a:pair[1]
    endif
endfunction

" delete pairs
inoremap <expr> <bs> <SID>DeletePair()
function! s:DeletePair()
    let x = col('.') - 1
    let two_chars = getline('.')[x - 1 : x]
    let pairs = ['""', "''", '``', '()', '[]', '{}']

    if index(pairs, two_chars) >= 0
        return "\<BS>\<Del>"
    else
        return "\<BS>"
    endif
endfunction

" surround selection
smap " <C-G>s"``a
smap ' <C-G>s'``a
smap ` <C-G>s```a
smap * <C-G>s*``a
smap ( <C-G>s)``a
smap [ <C-G>s]``a
smap { <C-G>s}``a

" fix backspace and delete
snoremap <BS> .<BS>
smap <Del> <BS>
