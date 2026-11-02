#!/bin/sh
# git external diff driver for images: path old-file old-hex old-mode new-file new-hex new-mode
# Images are drawn on /dev/tty to bypass the pager.
path=$1 old=$2 new=$5

show() {
    chafa -f kitty "$1" > /dev/tty
}

if [ "$old" = /dev/null ]; then
    echo "$path: image added"
    show "$new"
elif [ "$new" = /dev/null ]; then
    echo "$path: image removed"
    show "$old"
else
    out=$(mktemp -d)/diff.png
    if odiff "$old" "$new" "$out"; then
        echo "$path: images are identical"
    else
        echo "$path: images differ"
        [ -f "$out" ] && show "$out"
    fi
fi
exit 0
