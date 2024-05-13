#-------
#  fzf
#  https://github.com/junegunn/fzf
#-------

export FZF_DEFAULT_COMMAND="ag -l '.'"
export FZF_DEFAULT_OPTS="--reverse"


# auto-completion
[[ $- == *i* ]] && source "$HOMEBREW_PREFIX/opt/fzf/shell/completion.zsh" 2> /dev/null

# key bindings
source "$HOMEBREW_PREFIX/opt/fzf/shell/key-bindings.zsh"
