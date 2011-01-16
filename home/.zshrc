#!/usr/bin/env sh

# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# https://github.com/narfdotpl/dotfiles


#--------
#  PATH
#--------

export PATH=~/bin\
:/usr/local/Cellar/python/2.7/bin\
:/usr/local/Cellar/ruby/1.9.2-p0/bin\
:/usr/local/bin\
:$PATH


#----------
#  CDPATH
#----------

# put handy symlinks here
export CDPATH=~/⚡


#------------
#  language
#------------

export LANG=en_US.UTF-8


#-----------------
#  GNU coreutils
#-----------------

# try to use GNU ls
if [[ -x "`which gls`" ]]; then
    ls() {gls "$@"}
fi

# try to use GNU sort
if [[ -x "`which gsort`" ]]; then
    sort() {gsort "$@"}
fi


#----------
#  editor
#----------

if [[ -x `which gvim` ]]; then
    export EDIT='gvim -p'  # -p == open tab for each file
    if [[ -x `which mvim` ]]; then  # gvim is symlink to mvim on my mac
        # go back to terminal after closing editor
        export EDITOR='sh -c "'$EDIT' --nofork $@ && open -a terminal"'
    else
        export EDITOR=$EDIT' --nofork'
    fi
else
    export EDIT='vim'
    export EDITOR=$EDIT
fi

# `edit .zshrc`, `echo foo | edit`, `edit` == `edit .`
edit() {
    # check if stdin refers to terminal
    if [[ -t 0 ]]; then
        if [[ "$@" = "" ]]; then
            eval "$EDIT ."
        else
            eval "$EDIT $@"
        fi
    else
        eval "$EDIT -"
    fi
}


#------
#  ls
#------

# display names in column, append type indicators and ignore
# compiled/optimized Python code and Vim swap
column_ls() {
    ls -1F $@ | awk '{
        if (!($0 ~ /\.(py[co]|sw[nop]).?$/))
            printf("%s\n", $0)
    }' | more
}


#--------------
#  completion
#--------------

autoload -U compinit && compinit

# make completion lists as compact as possible
setopt list_packed

# list by lines
setopt list_rows_first


#-----------
#  history
#-----------

# log 10k commands
HISTSIZE=10000
SAVEHIST=$HISTSIZE
HISTFILE=~/.zsh_history

# append to HISTFILE when command is typed
setopt inc_append_history

# log timestamps
setopt extended_history

# if command is preceded with a space, don't log it
setopt hist_ignore_space

# if command duplicates any older one, don't show older ones
setopt hist_ignore_all_dups

# if command duplicates the *previous* one, don't log it
setopt hist_save_no_dups


#-------------
#  zsh magic
#-------------

autoload -U zmv


#----------
#  prompt
#----------

# subject PROMPT string to parameter expansion, command substitution,
# and arithmetic expansion
setopt prompt_subst

# set colors
DEFAULT_COLOR=$'%{\e[0m%}'
GREY=$'%{\e[0;37m%}'
BLUE=$'%{\e[0;36m%}'  # I'm color blind, k?

# show short path, git repo info and ">" sign, e.g. "foo/bar/baz master > "
get_short_path() {python ~/.scripts/short_path.py "$(pwd)"}
get_git_prompt() {python ~/.scripts/git/prompt.py}
PROMPT='${BLUE}$(get_short_path)${GREY}$(get_git_prompt) ${DEFAULT_COLOR}> '

# show non-zero exit code
RPROMPT='%(0?..%?)'


#------------
#  bindings
#------------

# ctrl + a/e
bindkey '^a' beginning-of-line
bindkey '^e' end-of-line

# up/down arrow: ipython-like history
bindkey '^[[A' history-beginning-search-backward
bindkey '^[[B' history-beginning-search-forward

# forward delete
bindkey '^[[3~' delete-char


#-----------
#  aliases
#-----------

# load loop and script aliases
source ~/.loops/aliases.zsh
source ~/.scripts/aliases.zsh

# find html files
alias -g .html='`find . -name "*.html"`'

# find javascript files
alias -g .js='`find . -name "*.js"`'

# find python files
alias -g .py='`find . -name "*.py"`'

# run homebrew
alias b='brew'

# quietly update homebrew and list outdated tools
alias bu='brew update 2> /dev/null; brew outdated'

# change directory
c() {cd $1 > /dev/null}
compdef c=cd
alias ,='c -'
alias .='cd ..'
alias ..='cd ../..'
alias ...='cd ../../..'
alias /='cd -P .'

# clear terminal screen
alias cl='clear'

# copy (working directory) path
cpwd() {
    # get working directory path
    local _path="`pwd`"

    # append first argument to path
    if [[ "$1" != '' ]]; then
        _path="$_path/$1"
    fi

    # copy quoted path to clipboard
    echo -n "'$_path'" | pbcopy
}

# go to desktop
alias d='cd ~/Desktop'

# show date (example: 2009-11-07 01:16:21, Saturday)
alias da='date "+%Y-%m-%d %H:%M:%S, %A"'

# deactivate virtualenv
alias de='deactivate'

# edit
alias e='edit'

# edit files (and directories) returned by previous command (I use this
# after `grep --files-with-matches`)
alias ee='edit $(fc -e - 2> /dev/null)'

# find in working directory without expanding wildcards
# http://www.chiark.greenend.org.uk/~sgtatham/aliases.html
f_helper() {
    find . -name "$@"
    setopt glob
}
alias f='setopt noglob; f_helper'

# flush dns
alias flushdns='dscacheutil -flushcache'

# run git
alias g='git'
git() {hub "$@"}  # https://github.com/defunkt/hub

# grep for file names
alias GF='grep --files-with-matches'
alias gf='GF --ignore-case'

# grep through shell history
alias GH='history -i 1 | grep'
alias gh='GH --ignore-case'

# grep
alias GR='grep --line-number'
alias gr='GR --ignore-case'

# go to ~/dotfiles/home
alias h='c home'

# show shell history
alias his='history -i 1 | less +G'

# run JSLint
alias jslint='java -jar ~/tools/rhino.jar ~/tools/jslint.js'

# list directory contents
alias l='column_ls'
alias l/='column_ls -d *(/)'  # directories
alias l.='column_ls -d *(.)'  # files
alias l@='column_ls -d *(@)'  # links
alias .l='column_ls -d .*'    # hidden stuff

# create directory (and intermediate directories) and go there
m() {mkdir -p $1 && cd $1}

# refresh memory https://github.com/jpalardy/forgetful
alias mem='rlwrap forgetful `ls ~/forgetful/*.csv | sort --random-sort`'

# run python
alias p='python -3'
alias py='python'
alias p3='python3'

# ping google
alias pg='ping -c 5 google.com'

# install python package
alias pi='pip install'

# remove *.pyc files
alias pyc='find . -name "*.pyc" -delete'

# run pyflakes
alias pyf='pyflakes `find . -name "*.py"`'

# brutally remove
alias rf='rm -rf'

# remove TeX mess
alias rmx='rm *.(aux|fdb_latexmk|log|nav|out|snm|synctex.gz|toc)'

# go to sandbox
alias s='cd ~/sandbox'

# save workspace
alias save='save_workspace'

# edit todo
alias t='edit ~/Dropbox/todo.taskpaper'

# locate app
alias wh='which'

# activate virtualenv
alias wo='workon'

# edit *this* file
alias z='edit ~/.zshrc'

# schedule sleep
zzz() {
    echo "osascript -e 'tell application \"System Events\" to sleep'" | at $@
}


#----------
#  python
#----------

export PYTHONSTARTUP=~/.pythonrc.py

# pip
export PIP_RESPECT_VIRTUALENV=true
eval `pip completion --zsh`

# virtualenv
source ~/.virtualenvs/virtualenvwrapper_bashrc


#--------
#  ruby
#--------

export RUBYOPT=rubygems


#---------------
#  local stuff
#---------------

[[ -f ~/.localrc ]] && source ~/.localrc


#--------
#  MOTD
#--------

# example: stallman (Linux), up 29 days
python ~/.scripts/show_machine_info.py MacBook.local


#------------
#  keychain
#------------

# https://github.com/funtoo/keychain
eval `keychain --eval --quiet --agents ssh id_rsa`


#-------------
#  workspace
#-------------

workspace=~/.workspace

# restore workspace (working directory and virtualenv) on startup
if [[ -f $workspace ]]; then
    source $workspace
    rm $workspace
fi

save_workspace() {
    echo "cd '`pwd`'" > $workspace
    if [[ $VIRTUAL_ENV != '' ]]; then
        echo "workon `basename $VIRTUAL_ENV`" >> $workspace
    fi
}
