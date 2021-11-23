#-------
#  fzf
#  https://github.com/junegunn/fzf
#-------

export FZF_DEFAULT_COMMAND="ag -l '.'"
export FZF_DEFAULT_OPTS="--reverse"


# auto-completion
[[ $- == *i* ]] && source "/usr/local/opt/fzf/shell/completion.zsh" 2> /dev/null

# key bindings
source "/usr/local/opt/fzf/shell/key-bindings.zsh"
