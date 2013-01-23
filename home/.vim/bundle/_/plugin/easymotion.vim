" use different leader
let g:EasyMotion_leader_key = '<Leader>\'

" map f for quick access
nmap f <Leader>\f

" map q for quick access
nmap q <Leader>\w
nmap Q <Leader>\b

" prefix original mappings with <Leader>
nnoremap <Leader>f f
nnoremap <Leader>q q
nnoremap <Leader>Q Q

" prefer keys closer to q
let g:EasyMotion_keys = 'qweasd1234xcrfvz'

" use stronger highlighting
hi link EasyMotionTarget Search
