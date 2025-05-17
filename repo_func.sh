#!/usr/bin/env bash
function check_folder_or_file_exist() {
	syncTARGET=$1
	# Check the last character of syncTARGET
	if [[ "${syncTARGET: -1}" == "/" ]]; then
		# If the last character is "/", check if it's a directory
		if [[ ! -d "$syncTARGET" ]]; then
      echo "[CreateNewFolder] $syncTARGET not found, create it"
			mkdir $syncTARGET
		fi
	fi
}

function ask_before_sync() {
	check_folder_or_file_exist $2

	syncSOURCE=$1
	syncTARGET=$2
	echo -e "\n\n[Source dir] $syncSOURCE"
	ls $syncSOURCE
	echo -e "\n\n[Target dir] $syncTARGET"
	ls $syncTARGET


	echo -e "\n[Will Backup] $syncSOURCE --> $syncTARGET"
	read -p "Press enter to sync folder"
	echo rsync -arvh $syncSOURCE $syncTARGET
	rsync -arvh $syncSOURCE $syncTARGET
}

ask_before_sync $1 $2
