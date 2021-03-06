#!/bin/bash

# Disc backup script
# Requires rsync 3

# Ask for the administrator password upfront
sudo -v

# IMPORTANT: Make sure you update the `DST` variable to match the name of the
# destination backup drive

DST="/Volumes/Backup"
SRC="/"
EXCLUDE="$HOME/.config/backup/excludes.txt"

PROG=$0

# --acls                   update the destination ACLs to be the same as the source ACLs
# --archive                turn on archive mode (recursive copy + retain attributes)
# --delete                 delete any files that have been deleted locally
# --delete-excluded        delete any files (on DST) that are part of the list of excluded files
# --exclude-from           reference a list of files to exclude
# --hard-links             preserve hard-links
# --one-file-system        don't cross device boundaries (ignore mounted volumes)
# --sparse                 handle spare files efficiently
# --progress               show progress during transfer
# --xattrs                 update the remote extended attributes to be the same as the local ones

if [ ! -r "$SRC" ]; then
    logger -t $PROG "Source $SRC not readable - Cannot start the sync process"
    exit;
fi

if [ ! -w "$DST" ]; then
    logger -t $PROG "Destination $DST not writeable - Cannot start the sync process"
    exit;
fi

$LOGGER -t $PROG "Delete Caches"
find "$DST" -name Caches -exec rm -rf {} \;

$LOGGER -t $PROG "Start rsync"

sudo rsync --acls \
           --archive \
           --delete \
           --delete-excluded \
           --exclude-from=$EXCLUDE \
           --hard-links \
           --one-file-system \
           --sparse \
           --progress \
           --xattrs \
           "$SRC" "$DST"

logger -t $PROG "End rsync"

# Make the backup bootable
sudo bless -folder "$DST"/System/Library/CoreServices

exit 0
