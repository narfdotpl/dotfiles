# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# http://github.com/narfdotpl/dotfiles


#--------
#  PATH
#--------

PORT_PATH=/opt/local/bin:/opt/local/sbin
POSTGRES_PATH=/Library/PostgreSQL/8.3/bin/
PYTHON_PATH=/Library/Frameworks/Python.framework/Versions/2.6/bin

PATH=$PORT_PATH:$POSTGRES_PATH:$PYTHON_PATH:$PATH


#--------------
#  completion
#--------------

autoload -U compinit
compinit

# make completion lists as compact as possible
setopt list_packed


#-----------
#  history
#-----------

# remember 2000 commands
HISTSIZE=2000
SAVEHIST=$HISTSIZE
HISTFILE=~/.zsh/history

# append to HISTFILE when command is typed
setopt inc_append_history

# save timestamps
setopt extended_history

# don't log commands that begin with a space
setopt hist_ignore_space

# if command duplicates any older one, don't show the older one
setopt hist_ignore_all_dups

# if command duplicates the *previous* one, don't add it to the HISTFILE
setopt hist_save_no_dups


#----------
#  prompt
#----------

# put git branch name in shell prompt
#
# example:
#     ~ $ cd code/mungdaal
#     ~/code/mungdaal(master) $ cd tests
#     ~/code/mungdaal/tests(master) $ touch dummy; git add dummy
#     ~/code/mungdaal/tests(master+) $

git_status() {
    # original function: http://gist.github.com/31631
    if [[ \
        $(git status 2> /dev/null | tail -n 1) \
            != 'nothing to commit (working directory clean)'
    ]]; then
        echo '+'
    fi
}

git_branch_name() {
    # original function: http://gist.github.com/5129
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
}

git_prompt() {
    typeset current_git_branch_name=$(git_branch_name)
    if [[ $current_git_branch_name != '' ]]; then
        echo "($current_git_branch_name$(git_status))"
    fi
}

# subject PROMPT string to parameter expansion, command substitution
# and arithmetic expansion
setopt prompt_subst

# show three trailing components of current path (replace $HOME with ~),
# git prompt and dollar sign
PROMPT='%3~$(git_prompt) $ '


#-----------
#  aliases
#-----------

# change directory
alias c='cd'
alias .='cd ..'
alias ..='.; .'
alias ...='.; .; .'

# clear
alias cl='clear'

# copy working directory path
alias cpwd='pwd | tr -d "\n" | pbcopy'

# run MacVim
alias e='mvim'

# show shell history
alias h='history -i'

# list directory contents
alias l='ls -F'
alias l/='ls -dF *(/)'  # directories
alias l.='ls -dF *(.)'  # files
alias l@='ls -dF *(@)'  # links

# list directory contents that begin with a dot
alias .l='ls -dF .*'
alias .l/='ls -dF .*(/)'  # directories
alias .l.='ls -dF .*(.)'  # files
alias .l@='ls -dF .*(@)'  # links

# open directory in finder
alias lo='open `pwd`'

# create directory (and intermediate directories) and go there
m() {
    mkdir -p $1
    cd $1
}

# run Python
alias p='python'
alias p3='python3'

# remove *.pyc files
alias pyc='rm `find . -name "*.pyc"`'

# run PyFlakes
alias pyf='pyflakes `find . -name "*.py"`'

# run Ruby
alias r='ruby'

# run scripts
alias kil='python ~/.scripts/kil.py'
alias lcs='python ~/.scripts/loop_c-sharp.py'
alias lnt='python ~/.scripts/loop_nosetests.py `find . -name "*.py"`'
alias lp='python ~/.scripts/loop_python.py'
alias lp3='python ~/.scripts/loop_python3.py'
alias lr='python ~/.scripts/loop_ruby.py'
alias mp3='python ~/.scripts/rename_mp3s.py'
alias o='python ~/.scripts/proxy_open.py'


#----------
#  Python
#----------

export PYTHONSTARTUP=~/.pythonrc.py


#------------------------------------
#  private stuff (SSH aliases etc.)
#------------------------------------

[[ -f ~/.zsh/private ]] && source ~/.zsh/private

