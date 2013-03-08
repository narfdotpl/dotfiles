" use ~60 FPS
let g:sexyscroll_update_display_per_milliseconds=16

" scroll one screen up/down
nnoremap Q :call g:sexyscroll('up', &lines, 200)<Enter>
nnoremap E :call g:sexyscroll('down', &lines, 200)<Enter>

" prefix original mappings with <Leader>
nnoremap <Leader>Q Q
nnoremap <Leader>E E
