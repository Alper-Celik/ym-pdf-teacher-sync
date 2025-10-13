import os
from get_files import get_files
import json
import tempfile
import subprocess
import selenium.common.exceptions


def load_sources():
    with open("sources.json", "r") as file:
        return json.load(file)


def main():
    sources = load_sources()
    for key in sources:
        source = sources[key]
        print(f"> source {key} = {source}")
        retries = 5
        for i in range(retries):
            try:
                get_and_upload(key, source)
                break
            except selenium.common.exceptions.TimeoutException:
                print(f"\n>> timeout error, remaining retries : {retries - i - 1}\n")
                pass
                if (i - 1) == retries:
                    raise selenium.common.exceptions.TimeoutException()


def get_and_upload(key, source):
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
