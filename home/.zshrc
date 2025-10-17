# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# https://github.com/narfdotpl/dotfiles


#------------
#  language
#------------

export LANG=en_US.UTF-8
export LC_ALL=$LANG


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


#-------
#  fzf
#-------

source ~/.fzf.zsh


#--------------
#  completion
#--------------

# use completion provided by homebrew
fpath=($HOMEBREW_PREFIX/share/zsh/site-functions $fpath)

# init
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

# show short path, git info and ">" sign
PROMPT='${BLUE}%3~${GREEN}$(~/.scripts/git/prompt/git-prompt) ${WHITE}>${DEFAULT} '

# show non-zero exit code
RPROMPT='${RED}%(0?..%?)${DEFAULT}'

# iTerm tab title: repo name
precmd() {
    local _path=$(git rev-parse --show-toplevel 2> /dev/null || dirs)
    local title=$(basename $_path)
    echo -ne "\033]0;"$title"\007"
}


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

# alias and
alias -g :='&&'

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

# ag
alias agg="ag -l '.' | ag"
alias agl='ag --nocolor -l'

# ag | peat
ap() {
    ag -g . | peat -i 500 "$*"
}

# go to login screen
alias a='afk'
alias ae='afk; exit'
alias afk='tell spotify to pause && suspend && pmset displaysleepnow'
alias suspend='/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend && sleep 4'

# run homebrew
alias b='brew'

# quietly update homebrew and list outdated tools
alias bu='brew update 2> /dev/null; brew outdated'

# change directory
c() {cd $1 > /dev/null}
compdef c=cd
alias ,='c -'
alias ..='cd ../..'
alias ...='cd ../../..'
alias /='cd -P .'

# change directory or source file
.() {
    if [ $# -eq 0 ]; then
        cd ..
    else
        source "$@"
    fi
}

# run calendar
alias ca='cal'

# change directory to the one opened in finder
alias cc='c "`tell finder to get the name of the first window`"'

# use fuzzy search to change directories
cf() {
    cd "$(fd --type d | fzf || echo .)"
}

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
alias de='pyenv deactivate'

# show date and time (example: 2011-06-04 09:54:07, Saturday)
alias dt='date "+%Y-%m-%d %H:%M:%S, %A"'

# show duplicate lines, e.g.: `ag --nofilename '^class' | dup`
alias dup='sort | uniq -D | uniq'

# edit
alias e='edit'

# edit files (and directories) returned by previous command (I use this
# after `ag --files-with-matches`)
alias ee='edit $(fc -e - 2> /dev/null)'

# edit file selected with fzf
ef() {
    local file="$(fzf -0 -1 -q "$*")"
    [[ "$file" != "" ]] && edit "$file"
}

# edit .gitconfig
alias eg='(h && e .config/git/config)'

# edit .vimrc
alias ev='(h && e .vimrc)'

# exit
alias ex='exit'

# edit *this* file
alias ez='(h && e .zshrc)'

# open Things
alias f="open 'things:///show?id=today&filter=focus'"
alias ff="open 'things:///show?id=anytime&filter=priorytet'"
alias fff="open 'things:///show?id=anytime&filter=focus'"
alias fk="open 'things:///show?id=anytime&filter=focus,komputer'"
alias fn="open 'things:///show?id=today&filter=now'"

# find with fuzzy matching
fdf() {
    fd | fzf -1 -q "$*"
}

# flush dns
alias flushdns='dscacheutil -flushcache'

# screw you, Docker
fudocker() {
    docker image prune --all
    docker system prune
}

# screw you, Xcode
fuxcode() {
    quit simulator
    quit xcode
    rm -rf ~/Library/Developer/Xcode/DerivedData
    sudo rm -rf /System/Library/Caches/com.apple.coresymbolicationd
    snapshot reset_simulators
    # sudo reboot
}

# change video to gif (QuickTime Player, File, New Screen Recording)
gifify() {
    local gif=${1%.*}.gif

    ffmpeg -i $1 -pix_fmt rgb24 -r 25 -f gif - 2> /dev/null |
    gifsicle --scale=0.5 --optimize=3 --delay=4 > $gif

    qlmanage -p $gif > /dev/null 2>&1
}

# run git (use git log alias if no arguments are given)
g() {
    if [ $# -eq 0 ]; then
        git l
    else
        git "$@"
    fi
}

# go to ~/dotfiles/home
alias h='c home'

# start http server
alias http='open http://`ip`:8000/; python3 -m http.server'

# get local IP addresses
alias ip="ifconfig | ag 'inet 192' | awk '{ print \$2 }' | sort -u"

# list directory contents
alias ll='ls -Fal --time-style=long-iso | more'
alias l='column_ls'
alias l/='column_ls -d *(/)'  # directories
alias l.='column_ls -d *(.)'  # files
alias l@='column_ls -d *(@)'  # links
alias .l='column_ls -d .*'    # hidden stuff

# create directory (and intermediate directories) and go there
m() {mkdir -p $1 && cd $1}

# exclude matching lines
alias not='ag --invert-match'

# open
o() {
    if [ $# -eq 0 ]; then
        open .
    else
        open $*
    fi
}

# run python
alias p='python3'

# activate virtualenv
alias pa='pyenv activate $(basename $(pwd))'

# use paste board without ⇥
alias pbc='pbcopy'

# list installed python packages
alias pf='pip freeze'

# ping google
alias pg='ping -c 5 google.com'

# install python package
alias pi='pip install'

# don't type so much when working on my websites
alias r='pa; ./manage.py runserver'

# quit an app
quit() { tell $1 to quit }

# reload safari
reload-safari() {
    ag -l . | peat -i 500 "tell Safari to 'do JavaScript \"window.location.reload()\" in front document'"
}

# brutally remove
alias rf='rm -rf'

# go to sandbox
alias s='cd ~/sandbox'

# save workspace
alias save='save_workspace'

# go to a temporary directory on the desktop
alias t='m ~/Desktop/tmp'

# show TODOs added in the current branch
alias todo='g diff master...HEAD | ag "^\+" | ag TODO'

# open Cursor
v() {
    if [[ "$@" = "" ]]; then
        cursor . || code .
    else
        cursor $@ || code $@
    fi
}

# locate app
alias wh='which'

# open Xcode project(s)
alias x='open "$(ls | ag .xcworkspace$ || ls | ag .xcodeproj$ || ls | ag .playground$)"'

# (schedule) sleep
# read `man atrun` to enable scheduling
alias z='zzz'
zzz() {
    local cmd="tell 'System Events' to sleep"
    if [[ "$@" = "" ]]; then
        eval $cmd
    else
        echo $cmd | at $@
    fi
}

# sleep and close terminal
alias ze='zzz; exit'


#----------
#  python
#----------

# wrapped in an one-off function to lazy-load on first use
pyenv() {
    unset -f pyenv
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    pyenv "$@"
}

# pip
export PIP_DOWNLOAD_CACHE=~/.pip/download-cache
export PIP_RESPECT_VIRTUALENV=true


#-------
#  bun
#-------

source ~/.bun/_bun


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
        echo "pyenv activate `basename $VIRTUAL_ENV`" >> $workspace
    fi
}
