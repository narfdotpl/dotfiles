" open readonly vim window with `git show <sha>`
map <buffer> <Space> V<Esc>:silent '<,'>w ! awk '{ print $2 }'
                                       \ \| xargs git show \| gvim -R -
                                       \ <Enter><Enter>
