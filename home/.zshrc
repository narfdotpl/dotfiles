#!/usr/bin/env sh

# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# http://github.com/narfdotpl/dotfiles


#--------
#  PATH
#--------

export PATH=~/bin\
:/usr/local/Cellar/python/2.7/bin\
:/Library/PostgreSQL/8.4/bin\
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

edit() {
    if [[ "$@" = "" ]]; then
        local stdin
        local part

        read stdin
        while read part; do
            stdin+="\n"$part
        done

        echo "$stdin" | eval "$EDIT -"
    else
        eval "$EDIT $@"
    fi
}


#------
#  ls
#------

# try to use GNU ls
if [[ -x `which gls` ]]; then
    ls() {gls "$@"}
fi

# append type indicator, ignore "./", "../", compiled/optimized Python code
# and Vim swap (with type indicators)
column_ls() {
    ls -F $@ | awk '{
        for (i=1; i<=NF; i++)
            if (!($i ~ /(^\.\.?\/|\.(py[co]|sw[nop]).?)$/))
                printf("%s\n", $i)
    }' | more
}


#--------------
#  completion
#--------------

autoload -U compinit
compinit

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


#----------
#  prompt
#----------

# subject PROMPT string to parameter expansion, command substitution,
# and arithmetic expansion
setopt prompt_subst

PROMPT='$(python ~/.scripts/prompt.py "$(pwd)")'

# show non-zero exit code
RPROMPT='%(0?..%?)'


#------------
#  bindings
#------------

# ctrl + a/e
bindkey '^a' beginning-of-line
bindkey '^e' end-of-line


#-----------
#  aliases
#-----------

# run less
alias :='less'

# find html files
alias -g .html='`find . -name "*.html"`'

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
alias c.='cd -P .'

# clear the terminal screen
alias cl='clear'

# copy working directory path
cpwd() {
    # get working directory path
    local _path="`pwd`"

    # join path with first argument
    if [[ "$1" != '' ]]; then
        _path="$_path/$1"
    fi

    # copy quoted path to clipboard
    echo -n "'$_path'" | pbcopy
}

# go to Desktop
alias d='cd ~/Desktop'

# show date (example: 2009-11-07 01:16:21, Saturday)
alias da='date "+%Y-%m-%d %H:%M:%S, %A"'

# deactivate virtualenv
alias de='deactivate'

# edit
alias e='edit'

# run git
alias g='git'
git() {hub "$@"}  # http://github.com/defunkt/hub

# run grep
alias gr='grep --ignore-case --line-number'

# grep for file names
alias gf='grep --ignore-case --files-with-matches'

# experiment using GraphicsMagick convert
#
# example:
#
#     gmc photo.jpg -rotate 90
#     gmc photo.jpg -rotate 90 -resize 50%
#     gmc apply photo.jpg -rotate 90 -resize 50%
#
gmc() {
    if [[ $1 == 'apply' ]]; then
        shift
        local destination=$1
    else
        local destination='/tmp/gmc.jpg'
    fi

    gm convert $@ $destination
    open $destination
}

# go to ~/dotfiles/home
alias h='c home'

# show shell history
alias hi='history -i 1 | less +G'

# run JSLint
alias jslint='java -jar ~/tools/rhino.jar ~/tools/jslint.js'

# list directory contents
alias l='column_ls'
alias l/='column_ls -d *(/)'  # directories
alias l.='column_ls -d *(.)'  # files
alias l@='column_ls -d *(@)'  # links
alias .l='column_ls -d .*'    # hidden stuff

# list directory contents using long listing format, don't ignore hidden
# files, don't list owner nor group, print sizes in human readable
# format (use powers of 1000 not 1024)
alias ll='ls --almost-all -g --no-group --si | less'

# create directory (and intermediate directories) and go there
m() {
    mkdir -p $1
    cd $1
}

# optimize png
alias op='optipng'

# run python
alias p='python -3'
alias py='python'
alias p3='python3'

# ping google
alias pg='ping -c 5 google.com'

# remove *.pyc files
alias pyc='rm `find . -name "*.pyc"`'

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

# edit todo list and commit previous changes
t() {
    # set paths
    local dir="$HOME/todo"
    local list="$dir/list.taskpaper"
    local gdir="--git-dir=$dir/.git"
    local wtree="--work-tree=$dir"

    # commit previous changes
    local mtime="`stat -f %m $list`"
    local isomtime="`date -j -f %s $mtime '+%Y-%m-%d %H:%M:%S'`"
    local diffstat="`git $gdir $wtree diff --stat | head -n 1 | cut -c 19-80`"
    git $gdir $wtree commit --all --message "$isomtime $diffstat" > /dev/null

    # edit list
    edit $list
}

# convert tabs to 4 spaces
alias t4s="perl -pi -e 's/\t/    /g'"

# locate program
alias wh='which'

# remove trailing whitespace http://gist.github.com/227361
alias ws="perl -pi -e 's/ +$//'"

# edit .zshrc
alias z='edit ~/.zshrc'


#-----------
#  scripts
#-----------

# run script
script() {
    # get python version
    if [[ $1 == '3' ]]; then
        local ver='3'
        shift
    else
        local ver=''
    fi

    # get script name
    local name=$1
    shift

    # run
    python$ver ~/.scripts/$name.py $@
}

alias .tar.bz2='script create_archive tar.bz2'
alias .zip='script create_archive zip'
alias 3='script publish_screenshot'
alias a2='script a2'
alias dcp='script public_dropbox copy'
alias dl='script download'
alias dmv='script public_dropbox move'
alias duration='script show_movie_duration'
alias gsay='script google_say'
alias kil='script kil'
alias mp3='script 3 convert_to_mp3'
alias mp4='script 3 convert_to_iphone_mp4'
alias mvt='script move_to_trash'
alias o='script proxy_open'
alias q='script quicklook'
alias r='script run_ruby'


#---------
#  loops
#---------

alias la='loop assembler'
alias lc='loop c'
alias lch='loop chrome'
alias lcs='loop c-sharp'
alias lj='loop javascript'
alias lm='loop markdown'
alias lno='loop nose `find . -name "*.py"`'
alias lo='loop octave'
alias lp='loop python'
alias lpy='loop python_wo_p3_warnings'
alias lp3='loop python3'
alias lr='loop ruby'
alias lsa='loop safari'
alias lx='loop xetex'


#------------
#  keychain
#------------

# http://github.com/funtoo/keychain
eval `keychain --eval --quiet --agents ssh id_rsa`


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


#-------------
#  workspace
#-------------

workspace=~/.workspace

# restore workspace (working directory and virtual env) on startup
if [[ -f $workspace ]]; then
    source $workspace
    rm $workspace
fi

save_workspace() {
    echo "cd '`pwd`'" > $workspace
    if [[ $VIRTUAL_ENV != '' ]]; then
        echo "source '$VIRTUAL_ENV/bin/activate'" >> $workspace
    fi
}
