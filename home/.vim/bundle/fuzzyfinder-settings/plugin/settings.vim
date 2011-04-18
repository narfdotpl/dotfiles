" make backspace act normally
let g:fuf_smartBs = 0

" don't show preview
let g:fuf_previewHeight = 0

" ignore backups, compiled/optimized Python code, Vim swap and SCM directories
let g:fuf_file_exclude = '\v\~$|\.(py[co]|sw[nop])$|(^|[/\\])\.(hg|git|bzr)($|[/\\])'


" open file starting from current file's directory
" http://vimcasts.org/episodes/the-edit-command/

" :e
map <Leader>E :e <C-R>=expand('%:p:h').'/'<Enter>
map <Leader>e
  \ :let g:fuf_file_prompt = ':e []'<Enter>
   \:let g:fuf_keyOpen = "<Enter\>"<Enter>
   \:exec 'FufFile '.expand('%:p:h').'/'<Enter>

" :sp
map <Leader>S :sp <C-R>=expand('%:p:h').'/'<Enter>
map <Leader>s
  \ :let g:fuf_file_prompt = ':sp []'<Enter>
   \:let g:fuf_keyOpenSplit = "<Enter\>"<Enter>
   \:exec 'FufFile '.expand('%:p:h').'/'<Enter>
   \:let g:fuf_keyOpenSplit = "<C-j\>"<Enter>

" :tabnew
map <Leader>T :tabnew <C-R>=expand('%:p:h').'/'<Enter>
map <Leader>t
  \ :let g:fuf_file_prompt = ':tabnew []'<Enter>
   \:let g:fuf_keyOpenTabpage = "<Enter\>"<Enter>
   \:exec 'FufFile '.expand('%:p:h').'/'<Enter>
   \:let g:fuf_keyOpenTabpage = "<C-l\>"<Enter>

" :vsp
map <Leader>V :vsp <C-R>=expand('%:p:h').'/'<Enter>
map <Leader>v
  \ :let g:fuf_file_prompt = ':vsp []'<Enter>
   \:let g:fuf_keyOpenVsplit = "<Enter\>"<Enter>
   \:exec 'FufFile '.expand('%:p:h').'/'<Enter>
   \:let g:fuf_keyOpenVsplit = "<C-k\>"<Enter>
