# run Z shell
zsh_bin="`which zsh`"
if [[ -x $zsh_bin ]]; then
    exec $zsh_bin --login
else
    echo "zsh not found, get it at http://www.zsh.org/"
fi
