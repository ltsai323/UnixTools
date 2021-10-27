#!/usr/bin/env bash

# If no parameter supplied, exit with usage help
if [ -z "$1" ]; then
  echo
  echo "    Usage: $0 /path/to/file"
  echo
  exit 1;
fi

# If the file supplied does not exists or cannot be readable
if [ ! -r "$1" ]; then
  echo "file \"${1}\" not found or couldn't read"
  exit 1;
fi

path=$1
fullname="${path##*/}"
dirname="${path%/*}"
basename="${fullname%.*}"
extension="${fullname##*.}"

# If the file is in the same directory with the script,
# path likely will not include any directory seperator.
if [ "$dirname" == "$path" ]; then
  dirname="."
fi

# If the file has no extension, correct the variable accordingly.
if [ "$extension" == "$basename" ]; then
  extension=""
fi

# Print parts
echo $basename
