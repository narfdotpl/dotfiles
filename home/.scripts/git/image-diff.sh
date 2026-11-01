#!/bin/sh
# git external diff driver for images: path old-file old-hex old-mode new-file new-hex new-mode
path=$1 old=$2 new=$5

if [ "$old" = /dev/null ] || [ "$new" = /dev/null ]; then
    echo "$path: image added or removed"
    exit 0
fi

out=$(mktemp -d)/diff.png
if odiff "$old" "$new" "$out"; then
    echo "$path: images are identical"
else
    echo "$path: images differ"
    [ -f "$out" ] && open "$out"
fi
exit 0
