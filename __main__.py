import os
from get_files import get_files
import json
import tempfile
import subprocess


def load_sources():
    with open("sources.json", "r") as file:
        return json.load(file)


def main():
    sources = load_sources()
    for key in sources:
        source = sources[key]
        print(f"> source {key} = {source}")
        with tempfile.TemporaryDirectory(key) as download_dir:
            get_files(source["url"], download_dir)
            subprocess.run(
                [
                    "./extract-and-upload.sh",
                    source["remote_dir"],
                    download_dir,
                    source["zip_dir"],
                ],
                check=True,
            )


if __name__ == "__main__":
    main()
