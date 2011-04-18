" reload font size settings
map <leader>f :FontsizedReload<Enter>

" change window size with alt + ctrl + arrow
map <A-C-up> :FontsizedTurnFullscreenOn<Enter>
map <A-C-right> :FontsizedUseTwoVerticalWindows<Enter>
map <A-C-down> :FontsizedTurnFullscreenOff<Enter>
map <A-C-left> :FontsizedUseOneVerticalWindow<Enter>
imap <A-C-up> <Esc><A-C-up>i
imap <A-C-right> <Esc><A-C-right>i
imap <A-C-down> <Esc><A-C-down>i
imap <A-C-left> <Esc><A-C-left>i
