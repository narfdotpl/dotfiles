" take advantage of TextMate muscle memory
nmap <D-/> gcc
imap <D-/> <Esc><D-/>a
vmap <D-/> gcgv
smap <D-/> <C-G><D-/><C-G>

" delete comment character when joining commented lines
set formatoptions+=j

" set missing comment strings
autocmd FileType gnuplot :set commentstring=#\ %s
autocmd FileType scheme :set commentstring=;\ %s
