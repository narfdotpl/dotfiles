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
    tmp=$(mktemp -d)
    out=$tmp/diff.png
    if odiff --diff-mask "$old" "$new" "$out"; then
        echo "$path: images are identical"
    else
        echo "$path: images differ (old, diff, new)"
        if [ -f "$out" ]; then
            set -- "$old" "$out" "$new"
        else
            set -- "$old" "$new"   # e.g. size mismatch: no diff image
        fi
        # landscape: stack vertically; portrait/square: side by side
        dims=$(magick identify -format '%w %h' "$new[0]" 2>/dev/null)
        w=${dims% *} h=${dims#* }
        if [ -n "$w" ] && [ "$w" -gt "$h" ]; then
            tile="1x$#"
        else
            tile="$#x1"
        fi
        if montage -background none -geometry '+6+6' -tile "$tile" "$@" "$tmp/all.png" 2>/dev/null; then
            show "$tmp/all.png"
        else
            for f in "$@"; do show "$f"; done
        fi
    fi
    rm -rf "$tmp"
fi
exit 0
