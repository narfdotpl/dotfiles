" remove blank lines and comments in rebase todo
autocmd BufEnter git-rebase-todo :silent g/\v^(#.*)?$/d | :normal gg0

" check my english in commit message
autocmd BufEnter COMMIT_EDITMSG :set spell spelllang=en
