# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# http://github.com/narfdotpl/dotfiles


#--------
#  PATH
#--------

export PATH=~/bin\
:/Library/Frameworks/Python.framework/Versions/2.6/bin\
:/Library/PostgreSQL/8.4/bin\
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

if [[ -x `which mvim` ]]; then
    export EDIT='mvim -p'  # -p == open tab for each file
    export EDITOR=$EDIT' --nofork'
else
    export EDIT='vim'
    export EDITOR=$EDIT
fi


#------
#  ls
#------

# try to use linux ls:
# check if `ls --version` exits with 0 status
ls --version > /dev/null 2>&1
if [[ $? = 0 ]]; then
    GNU_LS=true
# check if `gls` is present
elif [[ -x `which gls` ]]; then
    GNU_LS=true
    ls() {gls "$@"}
else
    GNU_LS=false
fi

# add default arguments
if [[ $GNU_LS = true ]]; then
    # append type indicator, list by lines
    # and ignore compiled/optimized Python code
    alias ls='ls -Fx --ignore="*.py[co]"'
else
    alias ls='ls -Fx'
fi


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

# log 10k commands
HISTSIZE=10000
SAVEHIST=$HISTSIZE
HISTFILE=~/.zsh/history

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

# alt + right/left arrow
bindkey '^[f' forward-word
bindkey '^[b' backward-word


#-----------
#  aliases
#-----------

# run less
alias :='less'

# run homebrew
alias b='brew'

# quietly update homebrew and list outdated tools
alias bu='brew update 2> /dev/null; brew outdated'

# change directory
c() {cd $1 > /dev/null}
compdef c=cd
alias ,='c -'
alias .='cd ..'
alias ..='.; .'
alias ...='.; .; .'

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

# cp/mv file to dropbox and copy public link to clipboard
alias dcp='dropbox cp'
alias dmv='dropbox mv'
dropbox() {
    $1 $2 ~/Dropbox/Public
    echo -n "http://▲.narf.pl/`basename $2`" | pbcopy
    # ▲.narf.pl/foo == dl.dropbox.com/u/2618196/foo
}

# edit
alias e=$EDIT

# run git
alias g='git'
git() {hub "$@"}  # http://github.com/defunkt/hub

# run grep
alias gr='grep --ignore-case'

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

# show shell history
alias h='history -i 1 | less +G'

# run JSLint
alias jslint='java -jar ~/tools/rhino.jar ~/tools/jslint.js'

# list directory contents
alias l='ls'
alias l/='ls -d *(/)'  # directories
alias l.='ls -d *(.)'  # files
alias l@='ls -d *(@)'  # links
alias .l='ls -d .*'    # hidden stuff


# create directory (and intermediate directories) and go there
m() {
    mkdir -p $1
    cd $1
}

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

# edit todo list
alias t="$EDIT ~/todo.taskpaper"

# convert tabs to 4 spaces
alias t4s="perl -pi -e 's/\t/    /g'"

# locate program
alias wh='which'

# remove trailing whitespace http://gist.github.com/227361
alias ws="perl -pi -e 's/ +$//'"

# edit .zshrc
alias z="$EDIT ~/.zshrc"


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
alias a2='script a2'
alias dl='script download'
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

# run loopozorg script
alias loop='python ~/.loops/loopozorg/script_runner.py'

alias la='loop assembler'
alias lc='loop c'
alias lch='loop chrome'
alias lcs='loop c-sharp'
alias lf='loop fabric'
alias lj='loop javascript'
alias lm='loop markdown'
alias lno='loop nose `find . -name "*.py"`'
alias lo='loop octave'
alias lp='loop python'
alias lpy='loop python_wo_p3_warnings'
alias lp3='loop python3'
alias lr='loop ruby'
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


#------------------------------------
#  private stuff (ssh aliases etc.)
#------------------------------------

[[ -f ~/.zsh/private ]] && source ~/.zsh/private


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
