" remove blank lines and comments in rebase todo
autocmd BufEnter git-rebase-todo :silent g/\v^(#.*)?$/d | :normal gg0

" widen commit message and diff windows
autocmd FileType git,gitcommit,diff
  \ :let &colorcolumn = &colorcolumn + 1 |
   \:let g:fontsized_next_columns = &columns + 1 |
   \:FontsizedReload

" check my english in commit message
autocmd BufEnter COMMIT_EDITMSG :set spell spelllang=en
