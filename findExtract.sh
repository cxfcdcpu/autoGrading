#/bin/sh
sleep 1
cd $1
ls
find . -name '*.tar.gz' -exec tar -xzvf {} \;
#rm *.gz
