" open readonly vim window with `git show <sha>`
map <buffer> <Space> V<Esc>:silent '<,'>w ! awk '{ print $1 }' \| tr -d ^
                                       \ \| xargs git show \| gvim -R -
                                       \ <Enter><Enter>
