#!/bin/bash

# Τhese are repo-specific, read only credentials. Don't even bother.
GITHUB_USERNAME="sourkitten"
GITHUB_TOKEN="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"
REPO="sourkitten/fytocomputer"
DIRECTORY="html"
LOCAL_DIRECTORY="/var/www/html"

# Download and extract the archive
archive_url="https://github.com/$REPO/trunk/$DIRECTORY/"
cp -r "$LOCAL_DIRECTORY/" "$LOCAL_DIRECTORY.bck/"
svn export --force --username $GITHUB_USERNAME --password $GITHUB_TOKEN --quiet $archive_url "$LOCAL_DIRECTORY/"