# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# http://github.com/narfdotpl/dotfiles


#--------
#  PATH
#--------

USER_PATH=~/bin
PORT_PATH=/opt/local/bin:/opt/local/sbin
POSTGRES_PATH=/Library/PostgreSQL/8.3/bin/
PYTHON_PATH=/Library/Frameworks/Python.framework/Versions/2.6/bin

PATH=$USER_PATH:$PORT_PATH:$POSTGRES_PATH:$PYTHON_PATH:$PATH


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


#--------
#  MOTD
#--------

# example: MacBook.local (Darwin), up 61 days
python ~/.scripts/show_machine_info.py


#----------
#  prompt
#----------

# Show git information in shell prompt.
#
# Show current branch name. If there were any changes since last commit, show
# a plus sign. If you are not in the top-level directory of the repository,
# precede branch name with one dot for every directory below the top.
#
# example:
#     ~ $ cd dotfiles
#     ~/dotfiles(master) $ cd .scripts
#     ~/dotfiles/.scripts(.master) $ touch dummy; git add dummy
#     ~/dotfiles/.scripts(.master+) $

_git_branch() {
    # original function: http://gist.github.com/5129
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
}

_git_dirty() {
    # original function: http://gist.github.com/31631
    local status_="`git status 2> /dev/null | tail -n 1`"
    if [[ $status_ != 'nothing to commit (working directory clean)' ]]; then
        echo '+'
    fi
}

_git_distance() {
    local prefix=".`git rev-parse --show-prefix 2> /dev/null`"
    while [[ $prefix != '.' ]]; do
        echo -n '.'
        prefix="`dirname $prefix`"
    done
}

_git_prompt() {
    local branch="`_git_branch`"
    if [[ $branch != '' ]]; then
        echo "(`_git_distance`$branch`_git_dirty`)"
    fi
}

# subject PROMPT string to parameter expansion, command substitution
# and arithmetic expansion
setopt prompt_subst

# show three trailing components of current path (replace $HOME with ~),
# git prompt and dollar sign
PROMPT='%3~`_git_prompt` $ '


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

# show date (example: 2009-11-07 01:16:21, Saturday)
alias d='date "+%Y-%m-%d %H:%M:%S, %A"'

# run MacVim
alias e='mvim'

# show shell history
alias h='history -i 1 | less +G'

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

# create directory (and intermediate directories) and go there
m() {
    mkdir -p $1
    cd $1
}

# run python
alias p='python'
alias p3='python3'

# remove *.pyc files
alias pyc='rm `find . -name "*.pyc"`'

# run pyflakes
alias pyf='pyflakes `find . -name "*.py"`'

# run less
alias s='less'

# run scripts
alias kil='python ~/.scripts/kil.py'
alias lcs='python ~/.scripts/loop_c-sharp.py'
alias lnt='python ~/.scripts/loop_nosetests.py `find . -name "*.py"`'
alias lp='python ~/.scripts/loop_python.py'
alias lp3='python ~/.scripts/loop_python3.py'
alias lr='python ~/.scripts/loop_ruby.py'
alias mp3='python ~/.scripts/rename_mp3s.py'
alias o='python ~/.scripts/proxy_open.py'
alias r='python ~/.scripts/run_ruby.py'


#------------
#  keychain
#------------

# http://github.com/funtoo/keychain
eval `keychain --eval --quiet --agents ssh id_rsa`


#----------
#  python
#----------

export PYTHONSTARTUP=~/.pythonrc.py


#------------------------------------
#  private stuff (ssh aliases etc.)
#------------------------------------

[[ -f ~/.zsh/private ]] && source ~/.zsh/private

