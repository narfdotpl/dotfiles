" take advantage of TextMate muscle memory
nmap <D-/> \\\
imap <D-/> <Esc><D-/>a
vmap <D-/> \\gv
smap <D-/> <C-G><D-/><C-G>

" set missing comment strings
autocmd FileType gnuplot :set commentstring=#\ %s
autocmd FileType scheme :set commentstring=;\ %s