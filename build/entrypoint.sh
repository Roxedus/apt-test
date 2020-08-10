#!/bin/bash

architectures=(amd64 arm64 armhf)

scriptPath=/scripts

cd "${scriptPath}" || exit 1

mkdir /out

safeVersion="${version#?}"

for arch in "${architectures[@]}"; do
    :

    versionDir="${arch}/builds/ombi-${safeVersion}"
    echo "Getting new build ${version}_${arch}"
    mkdir -p "$versionDir/ombi"

    python createDEBIAN.py "${arch}"

    # Copy the deb template to new version dir
    cp -r "templater/templates/debian" "${versionDir}/debian"

    # Download and extract linux.tar.gz to build folder
    case $arch in
    amd64)
        filename="linux-x64.tar.gz"
        ;;
    armhf)
        filename="linux-arm.tar.gz"
        ;;
    arm64)
        filename="linux-arm64.tar.gz"
        ;;
    esac

    curl -fsSL "https://github.com/tidusjar/Ombi.Releases/releases/download/${version}/${filename}" | tar xzf - -C "${versionDir}/ombi/"

    # Replace keywords in template changelog with actual values
    sed -i "${versionDir}/debian/changelog" -e "s/@{VERSION}/${safeVersion}/g" -e "s/@{MAINTAINER}/${maintainer}/g" -e "s/@{DATE}/$(date -R)/g"

    # Build the thing!
    cd "${versionDir}" || exit 1
    dpkg-buildpackage -b -us -uc -a "${arch}"
    cd "${scriptPath}" || exit 1
    cp "${arch}/builds/ombi_${safeVersion}_${arch}.deb" /out

    # If .deb was generated delete the build dir
done
