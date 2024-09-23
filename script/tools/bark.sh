#!/usr/bin/env sh
title=$1
content=$2

wget -nc "https://api.day.app/Qc9reVSUWxKgJ6cqNckgbB/${title}/${content}" -O aabark > /dev/null && mv aabark ~/latest_bark.txt
echo "[$title] $content"

