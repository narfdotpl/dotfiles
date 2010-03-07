# .zshrc -- Z shell configuration file
#
# Maciej Konieczny <hello@narf.pl>
# http://github.com/narfdotpl/dotfiles


#--------
#  PATH
#--------

export PATH=~/bin\
:/Library/Frameworks/Python.framework/Versions/2.6/bin\
:~/.gem/ruby/1.8/bin\
:/Library/PostgreSQL/8.4/bin\
:$PATH


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


#--------
#  MOTD
#--------

# example: stallman (Linux), up 29 days
python ~/.scripts/show_machine_info.py MacBook.local


#----------
#  prompt
#----------

# subject PROMPT string to parameter expansion, command substitution,
# and arithmetic expansion
setopt prompt_subst

# show three trailing components of current path (replace $HOME with ~),
# git prompt, and dollar sign
PROMPT='%3~$(python ~/.scripts/git/prompt.py) $ '

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

# run homebrew
alias b='brew'

# quietly update homebrew and list outdated tools
alias bu='brew update 2> /dev/null; brew outdated'

# change directory
alias c='cd'
alias ,='cd - > /dev/null'
alias .='cd ..'
alias ..='.; .'
alias ...='.; .; .'

# clear the terminal screen
alias cl='clear'

# copy working directory path
alias cpwd='pwd | tr -d "\n" | pbcopy'

# go to Desktop
alias d='cd ~/Desktop'

# show date (example: 2009-11-07 01:16:21, Saturday)
alias da='date "+%Y-%m-%d %H:%M:%S, %A"'

# edit
alias e=$EDIT

# run git
alias g='git'

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
alias p='python -3'
alias py='python'
alias p3='python3'

# ping google
alias pg='ping google.com'

# serve file via http http://www.home.unix-ag.org/simon/woof.html
alias pub='woof'

# remove *.pyc files
alias pyc='rm `find . -name "*.pyc"`'

# run pyflakes
alias pyf='pyflakes `find . -name "*.py"`'

# brutally remove
alias rf='rm -rf'

# remove TeX mess
alias rmx='rm *.(aux|fdb_latexmk|log|nav|out|snm|synctex.gz|toc)'

# run less
alias s='less'

# edit todo list
alias t="$EDIT ~/todo.taskpaper"

# convert tabs to 4 spaces
alias t4s="perl -pi -e 's/\t/    /g'"

# remove trailing whitespace http://gist.github.com/227361
alias ws="perl -pi -e 's/ +$//'"


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

alias a2='script a2'
alias duration='script show_movie_duration'
alias g1='script rename_g1_photos'
alias kil='script kil'
alias mp3='script rename_mp3s'
alias mp4='script 3 convert_to_iphone_mp4'
alias o='script proxy_open'
alias q='script quicklook'
alias r='script run_ruby'
alias rt='script move_to_trash'


#---------
#  loops
#---------

# run loopozorg script
alias loop='python ~/.loops/loopozorg/script_runner.py'

alias la='loop assembler'
alias lc='loop c'
alias lcs='loop c-sharp'
alias lf='loop fabric'
alias lj='loop javascript'
alias lno='loop nose `find . -name "*.py"`'
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


#------------------------------------
#  private stuff (ssh aliases etc.)
#------------------------------------

[[ -f ~/.zsh/private ]] && source ~/.zsh/private
