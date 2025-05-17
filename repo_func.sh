#!/usr/bin/env sh
function ask_before_sync() {
  syncSOURCE=`realpath $1`
  syncTARGET=`realpath $2`
  echo -e "\n\n[Source dir] $syncSOURCE"
  ls $syncSOURCE
  echo -e "\n\n[Target dir] $syncTARGET"
  ls $syncTARGET

  echo -e "\n[Will Backup] $syncSOURCE --> $syncTARGET"
  read -p "Press enter to sync folder"
  rsync -arvh $syncSOURCE $syncTARGET
}

ask_before_sync $1 $2
