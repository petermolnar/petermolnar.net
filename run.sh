#!/usr/bin/env bash

source .venv/bin/activate

rm rsync.* 2>/dev/null

set -Eeuao pipefail

excludes="$(mktemp rsync.XXXXXX)"
echo "
+ /
+ .secrets
+ .templates
- **/.*
- rsync.*
- __pycache__
" > "${excludes}"

source .secrets

python3 fetch.py

ARCHIVE=1
python3 build.py

rsync -avuh --progress --bwlimit=1000 --delete --filter="merge ${excludes}" ~/petermolnar.net/ liveserver:/usr/local/www/petermolnar.net/

rsync -avuh --delete --filter="merge ${excludes}" ~/petermolnar.net/ ~/www/
hardlink --verbose -O ~/petermolnar.net/ ~/www/

rm "${excludes}"
deactivate
