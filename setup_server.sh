#!/usr/bin/env bash

set -euo pipefail

github_account='CatalystCode'
github_repo='jp_tokenizer'
runcmd='run_server.py'
runas="$USER"
rootdir="$PWD"
python='python3.5'

# install mecab tokenizer
sudo apt-get install -y build-essential mecab mecab-ipadic libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y git
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
(cd mecab-ipadic-neologd; sudo ./bin/install-mecab-ipadic-neologd -n -y)

# install python
sudo apt-get install -y "${python}" "${python}-venv" "${python}-dev"

# install service
rootdir="${rootdir}/${github_account}-${github_repo}"
repo="${rootdir}/src"
venv="${rootdir}/env"
"${python}" -m venv "${venv}"
pip="${venv}/bin/pip"
python="${venv}/bin/python"
mkdir -p "${rootdir}"
git clone --depth 1 "https://github.com/${github_account}/${github_repo}.git" "${repo}"
"${pip}" install -U pip wheel
"${pip}" install -r "${repo}/requirements.txt"

# allow service to run on port 80
sudo apt-get install -y authbind
sudo touch '/etc/authbind/byport/80'
sudo chown "$runas:$runas" '/etc/authbind/byport/80'
sudo chmod 755 '/etc/authbind/byport/80'

# auto-start service
progname="$(basename ${rootdir})"
sudo apt-get install -y supervisor
sudo service supervisor start
sudo tee "/etc/supervisor/conf.d/${progname}.conf" << EOF
[program:${progname}]
command=/usr/bin/authbind '${python}' '${repo}/${runcmd}'
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/${progname}.err.log
stdout_logfile=/var/log/${progname}.out.log
user=$runas
environment=
EOF
sudo supervisorctl reread
sudo supervisorctl update
