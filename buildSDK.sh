#!/bin/sh

git clone http://dev.asyncode.com/git/acr.git
mv acr ACDK
cd ACDK
rm -rf .git debian test *.komodoproject *.kpf
git clone http://dev.asyncode.com/git/acfrontend.git
cd acfrontend
rm -rf .git debian *.komodoproject *.kpf
cd ..
mkdir projects
cd ..
zip -r ACDK.zip ACDK
tar -zcvf ACDK.tar.gz ACDK
