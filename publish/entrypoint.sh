#!/bin/bash

GPG_TTY=$(tty)
export GPG_TTY

#eval gpg-agent --batch --daemon
echo -e "${INPUT_GPG_PRIV}" | gpg --batch --import
echo "${INPUT_GPG_PASSPHRASE}" | gpg --batch --pinentry-mode loopback --passphrase-fd 0 --output /test --sign ./README.md

if [ "${INPUT_STATE}" != "unstable" ]; then
    comp="main"
else
    comp="develop"
fi

GPG_TTY=$(tty)
export GPG_TTY

find . -name '*.deb' -exec reprepro -VVb ./repo/metadata --outdir ./repo/public -C ${comp} includedeb jessie {} \;
