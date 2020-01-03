#!/usr/bin/env bash
# Simple installation script to make sure the latest version is in the user's PATH

thisName=ssl_test_ciphers.py
destDir=~/scripts/

echo "Copying script to ${destDir} directory..."
if [ -e ${destDir}/${thisName} ]; then
  echo "File exists! Overwriting..."
fi
cp ${thisName} ${destDir}
echo "Done!"
