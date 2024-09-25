#!/usr/bin/env bash
set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes

FILE_DIR="$(mktemp -d)"
echo $FILE_DIR
clean-tmp-dir(){
  rm -rf "${FILE_DIR}"
}
trap clean-tmp-dir EXIT


unzip-dir(){
  printf "\n\n>>unziping:\n"
  cd ./downloads
  unzip ./*.zip -d "${FILE_DIR}"
  printf "\n>>unzipped"
}

setup-rclone-cfg(){
  if [[ -v RCLONE_CONF_TEXT ]]; then 
    printf "\n\n>>creating rclone config: \n"
    echo "${RCLONE_CONF_TEXT}" > ~/.config/rclone/rclone.conf
    printf "\n>>created rclone config"
  fi
}

upload-folder(){
  printf "\n\n>>uploading files and folders:\n"
  cd "${FILE_DIR}/Algoritma ve Programlama 1"
  rclone sync -vvv --progress . "onedrive:/Ders pdf'leri/1. Dönem (1. Sene)/Algoritma ve Programlama 1/Hocanın Güncelledikleri"
  printf "\n>>uploaded files and folders"
}


unzip-dir
setup-rclone-cfg
upload-folder
