#!/bin/bash

echo -e "${INPUT_GPG_PRIV}" | gpg --batch --import

package=ombi
distro=jessie

if [ "${INPUT_STATE}" == "stable" ]; then
    branch="master"

else
    branch="develop"
fi

if [[ ! -d "./repo/${branch}/db" ]]; then
    aptly repo create -config="repo/${branch}.aptly.conf" -distribution="${distro}" "${package}"
fi

echo "Found debs: $(find . -path './builds/*' -name '*.deb')"

find . -path "./builds/*" -name '*.deb' -exec aptly repo add -config="repo/${branch}.aptly.conf" "${package}" {} \;

if [[ ! -d "./repo/public/${branch}/pool" ]]; then
    aptly publish repo -config="repo/${branch}.aptly.conf" -batch -passphrase="${INPUT_GPG_PASSPHRASE}" ombi filesystem:public:${branch}
else
    aptly publish update -config="repo/${branch}.aptly.conf" -batch -passphrase="${INPUT_GPG_PASSPHRASE}" "${distro}" filesystem:public:${branch}
fi
