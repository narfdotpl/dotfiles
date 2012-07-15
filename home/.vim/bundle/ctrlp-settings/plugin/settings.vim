" show max 5 matches, best at the top
let g:ctrlp_match_window_reversed = 0
let g:ctrlp_max_height = 5

" disable statusline
let g:ctrlp_status_func = {'main': 'CtrlP_Statusline_1'}
function! CtrlP_Statusline_1(...)
    return '%#Normal#'
endfunction

" ignore what needs to be ignored
let g:ctrlp_custom_ignore = {
  \ 'dir':  '\v^site_media$',
  \ 'file': '\v\.py[co]$',
  \ }

" invoke CtrlP
map <Leader>, :CtrlP<Enter>

" invoke CtrlP from current buffer's directory
map <Leader>. :CtrlP <C-R>=expand('%:p:h')<Enter><Enter>

" invoke CtrlP in find buffer mode
map <Leader>b :CtrlPBuffer<Enter>

" invoke CtrlP in find MRU file mode
map <Leader>m :CtrlPMRU<Enter>
