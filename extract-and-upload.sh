#!/usr/bin/env bash
set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

FILE_DIR="$(mktemp -d)"
DOWNLOAD_DIR="$2"
REMOTE_DIR="$1"
ZIP_DIR="$3"
echo "$FILE_DIR"
clean-tmp-dir() {
	rm -rf "${FILE_DIR}"
}
trap clean-tmp-dir EXIT

unzip-dir() {
	printf "\n\n>>unziping:\n"
	cd "$DOWNLOAD_DIR"
	ark --batch ./*.zip -o "${FILE_DIR}"
	printf "\n>>unzipped"
}

setup-rclone-cfg() {
	if [[ -v RCLONE_CONF_TEXT ]]; then
		printf "\n\n>>creating rclone config: \n"
		mkdir -p ~/.config/rclone
		echo "${RCLONE_CONF_TEXT}" >~/.config/rclone/rclone.conf
		printf "\n>>created rclone config"
	fi
}

upload-folder() {
	printf "\n\n>>uploading files and folders:\n"
	cd "${FILE_DIR}/${ZIP_DIR}"
	rclone sync -vvv --progress . "$REMOTE_DIR"
	printf "\n>>uploaded files and folders"
}

unzip-dir
setup-rclone-cfg
upload-folder
