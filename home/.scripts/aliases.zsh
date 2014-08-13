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

backup() {
    rm -rf ~/Library/Developer/Xcode/DerivedData
    sudo bash ~/.scripts/backup.bash
}

alias dcp='script public_dropbox copy'
alias dmv='script public_dropbox move'
alias duration='script show_movie_duration'
alias mp3='script 3 convert_to_mp3'
alias mp4='script 3 convert_to_iphone_mp4'
alias mvt='script move_to_trash'
alias o='script proxy_open'
