" launch fzf in iTerm
let g:fzf_launcher = "~/.vim/bundle/fzf/bin/iterm-macvim %s"

" use fzf from Homebrew
source /usr/local/opt/fzf/plugin/fzf.vim

" invoke FZF
map <Leader>, :FZF<Enter>

" invoke FZF from current buffer's directory
map <Leader>. :FZF <C-R>=expand('%:p:h')<Enter><Enter>
