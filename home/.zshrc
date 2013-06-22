# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# https://github.com/narfdotpl/dotfiles


# start with a fake prompt
echo -n '~ > '

# ensure iTerm is the frontmost app (without this when you are in some other
# app and you open a new terminal window with your mouse, that other other app
# remains the active one)
open -a iterm


#------------
#  language
#------------

export LANG=en_US.UTF-8


#-------------
#  GNU stuff
#-------------

# try to use GNU cal
if [[ -x "`which gcal`" ]]; then
    cal() {
        gcal --starting-day=monday --highlighting=\|:\| "$@" | grcat conf.gcal | tr '|' ' '
    }
fi

# try to use GNU ls
if [[ -x "`which gls`" ]]; then
    ls() {gls "$@"}
fi

# try to use GNU sort (with "version sorting" a'la OS X Finder)
if [[ -x "`which gsort`" ]]; then
    sort() {gsort --version-sort "$@"}
fi


#----------
#  editor
#----------

if [[ -x `which gvim` ]]; then
    export EDIT='gvim -p'  # -p == open tab for each file
    if [[ -x `which mvim` ]]; then  # gvim is symlink to mvim on my mac
        # go back to terminal after closing editor
        export EDITOR='sh -c "'$EDIT' --nofork \"$@\" && open -a iterm"'
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
            if [[ -f "Session.vim" ]]; then
                eval "$EDIT -S"
            else
                eval "$EDIT ."
            fi
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
    }' | sort | more
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

# set color names
DEFAULT=$'%{\e[0m%}'
RED=$'%{\e[0;31m%}'
GREEN=$'%{\e[0;32m%}'
BLUE=$'%{\e[0;34m%}'
WHITE=$'%{\e[0;37m%}'

# get git info for prompt
#
# full example: " ..master+&"
# (two dirs deep in repo, on branch master, dirty, with stashed changes)
git_prompt() {
    # check status and exit if there's no repo
    local status_dump="$(mktemp /tmp/git_prompt.XXXXXX)"
    trap "rm $status_dump" EXIT
    git status --porcelain > $status_dump 2> /dev/null
    [[ $? -gt 0 ]] && return

    # initial space
    echo -n ' '

    # depth
    git rev-parse --show-cdup | awk '{
        ORS = ""

        split($0, a, "/")
        depth = length(a) - 1
        while (depth --> 0)
            print "."
    }'

    # branch name
    git branch | sed -ne 's/* \(.*\)/\1/p' | tr -d '\n'

    # is dirty?
    [[ "$(head -c1 $status_dump)" != "" ]] && echo -n "+"

    # has stashed changes?
    [[ "$(git stash list | head -c1)" != "" ]] && echo -n "&"
}

# zsh has troubles displaying "⚡" with "PROMPT='%3~'", so...
short_pwd() {
    pwd | awk '{
        ORS = ""

        split($0, a, "/")
        a[3] = "~"

        len = length(a)
        start = len > 5 ? len - 2 : 3

        for (i = start; i <= len; i++) {
            print a[i]
            if (i != len)
                print "/"
        }
    }'
}

# show short path, git info and ">" sign
PROMPT='${BLUE}$(short_pwd)${GREEN}$(git_prompt) ${WHITE}>${DEFAULT} '

# show non-zero exit code
RPROMPT='${RED}%(0?..%?)${DEFAULT}'


#------------
#  bindings
#------------

# ctrl + a/e
bindkey '^a' beginning-of-line
bindkey '^e' end-of-line

# up/down arrow: ipython-like history
bindkey '^[[A' history-beginning-search-backward
bindkey '^[[B' history-beginning-search-forward

# alt + left/right: jump one word backward/forward
bindkey '^[^[[D' emacs-backward-word
bindkey '^[^[[C' emacs-forward-word

# forward delete
bindkey '^[[3~' delete-char


#-----------
#  aliases
#-----------

# load loop and script aliases
source ~/.loops/aliases.zsh
source ~/.scripts/aliases.zsh

# find webdev files
alias -g .coffee='`find . -name "*.coffee"`'
alias -g .css='`find . -name "*.css"`'
alias -g .eco='`find . -name "*.eco"`'
alias -g .html='`find . -name "*.html"`'
alias -g .js='`find . -name "*.js"`'
alias -g .pp='`find . -name "*.pp"`'
alias -g .py='`find . -name "*.py" | grep --invert-match migrations`'

# execute last command and use its output
#
# example:
#
#     > find . -name "foo*py"
#     ./qwe/rty/foobar.py
#     > git log ^
#     af2a1af added foobar.py
#
alias -g ^='$(fc -e - 2> /dev/null)'

# get nth word
#
# example:
#
#   > echo foo bar baz | 2
#   bar
#
alias 1="awk '{ print \$1 }'"
alias 2="awk '{ print \$2 }'"
alias 3="awk '{ print \$3 }'"
alias 4="awk '{ print \$4 }'"
alias 5="awk '{ print \$5 }'"

# go to login screen
alias a='afk'
alias afk='tell spotify to pause && /System/Library/CoreServices/Menu\ '\
'Extras/User.menu/Contents/Resources/CGSession -suspend && sleep 10'

# run homebrew
alias b='brew'

# smack my bishop
alias bitch,='sudo'

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

# copy directories without fuss
alias cp='cp -r'

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

# deactivate virtualenv
alias de='deactivate'

# run django
alias dj='clear; pyc; open -a "google chrome"; python manage.py runserver'

# show date and time (example: 2011-06-04 09:54:07, Saturday)
alias dt='date "+%Y-%m-%d %H:%M:%S, %A"'

# edit
alias e='edit'

# edit files (and directories) returned by previous command (I use this
# after `grep --files-with-matches`)
alias ee='edit $(fc -e - 2> /dev/null)'

# edit .gitconfig
alias eg='(h && e .config/git/config)'

# edit .vimrc
alias ev='(h && e .vimrc)'

# exit
alias ex='exit'

# edit *this* file
alias ez='(h && e .zshrc)'

# find in working directory without expanding wildcards
# http://www.chiark.greenend.org.uk/~sgtatham/aliases.html
f_helper() {
    find . -name "$@"
    setopt glob
}
alias f='setopt noglob; f_helper'

# don't type so much when using fabric
alias fh='fab -H'
alias fl='fh localhost'
alias fd='fl dev'
alias ft='fl test'

# flush dns
alias flushdns='dscacheutil -flushcache'

# run git
alias g='git'
git() {hub "$@"}  # https://github.com/defunkt/hub

# learn to live with typos
alias gL='g l'
alias gl='g l'

# grep for file names
alias GF='grep --files-with-matches --perl-regexp'
alias gf='GF --ignore-case'

# grep through shell history
alias GH='history -i 1 | grep --perl-regexp'
alias gh='GH --ignore-case'

# grep
alias GR='grep --perl-regexp'
alias gr='GR --ignore-case'

# go to ~/dotfiles/home
alias h='c home'

# start http server
alias http='open http://localhost:8000/; python -m SimpleHTTPServer'

# go to ideas
alias i='c ideas'

# pretty print json (`cat foo.json | json`)
alias json='python -mjson.tool | pygmentize -l js'

# list directory contents
alias ll='ls -Fal --time-style=long-iso | more'
alias l='column_ls'
alias l/='column_ls -d *(/)'  # directories
alias l.='column_ls -d *(.)'  # files
alias l@='column_ls -d *(@)'  # links
alias .l='column_ls -d .*'    # hidden stuff

# create directory (and intermediate directories) and go there
m() {mkdir -p $1 && cd $1}

# minimize terminal
min() {
    osascript -e '
        tell application "System Events"
            keystroke "m" using command down
        end tell
    '
}

# exclude matching lines
alias not='grep --ignore-case --invert-match --perl-regexp'

# finish work and go home
off() {
    (osascript -e 'tell application "Skype" to quit' &)
    (afk &)
    exit
}

# run python
alias p='python -3'
alias py='python'
alias p3='python3'

# list installed python packages
alias pf='pip freeze'

# ping google
alias pg='ping -c 5 google.com'

# install python package
alias pi='pip install'

# remove *.pyc files
alias pyc='find . -name "*.pyc" -delete'

# run pyflakes
alias pyf='pyflakes .py | not __init__.py'

# preview using quicklook
q() {qlmanage -p $* > /dev/null}

# play more promode
alias q3='(c ~/q3/repo && ./ioquake3.app/Contents/MacOS/ioquake3.ub +set fs_game cpma)'

# brutally remove
alias rf='rm -rf'

# remove ~/Desktop/tmp and close terminal
alias rft='rm -rf ~/Desktop/tmp && exit'

# open rss client
alias rss='open -a netnewswire'

# go to sandbox
alias s='cd ~/sandbox'

# save workspace
alias save='save_workspace'

# run scheme
alias scm='rlwrap scheme'

# search stack overflow
alias so='open https://www.google.com/search\?q=site:stackoverflow.com'

# go to temporary directory on the desktop
alias t='d && m tmp'

# do video business in ~/Desktop/tmp
alias tv='t && v'

# download video from youtube, vimeo, blip, etc. or play video files
# from the current folder in VLC
alias v='setopt noglob; v_helper'
v_helper() {
    setopt glob
    if [[ "$@" = "" ]]; then
        open -a vlc *.(mp4|avi|flv|mov|mkv)
        sleep 1
        tell spotify to pause
    else
        # start download in the background
        youtube-dl --no-part --title --continue --quiet $1 &

        # show title
        youtube-dl --get-title $1

        # bring download to the foreground
        fg %youtube-dl
    fi
}

# open (file in) vlc
alias vlc='open -a vlc'

# don't type so much when using vagrant
alias vs='vagrant suspend'
alias vss='vagrant ssh'
alias vu='vagrant up'

# go back to writing
alias w='c narf.pl && e && c content/posts && wo narf.pl'

# locate app
alias wh='which'

# activate virtualenv
alias wo='workon'

# open Xcode project(s)
alias x='open *.xcodeproj'

# (schedule) sleep
# read `man atrun` to enable scheduling
alias z='zzz'
zzz() {
    local cmd="osascript -e 'tell application \"System Events\" to sleep'"
    if [[ "$@" = "" ]]; then
        eval $cmd
    else
        echo $cmd | at $@
    fi
}


#----------
#  python
#----------

export PYTHONSTARTUP=~/.pythonrc.py

# pip
export PIP_DOWNLOAD_CACHE=~/.pip/download-cache
export PIP_RESPECT_VIRTUALENV=true
eval `pip completion --zsh`

# brew-pip
export PYTHONPATH=$(brew --prefix)/lib/python2.7/site-packages

# virtualenv
source /usr/local/share/python/virtualenvwrapper.sh


#--------
#  ruby
#--------

export RUBYOPT=rubygems


#---------------
#  local stuff
#---------------

[[ -f ~/.localrc ]] && source ~/.localrc


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


#-----------
#  cleanup
#-----------

# clear the screen (I might've started typing before prompt was visible)
clear
