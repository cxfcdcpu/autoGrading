homeDir=~/Desktop
homeDir=${4:-$homeDir}
rc=19
url='rc'$rc'xcs213.managed.mst.edu'
user='cpp'
homeClass=$homeDir'/'$1
homeAss=${4:-$homeDir}'/'$1'/'$2
homeSect=${4:-$homeDir}'/'$1'/'$2'/'$3
./changeDir.sh $homeDir $homeAss $homeSect
scp -r $user'@rc'$rc'xcs213.managed.mst.edu:~/SDRIVE/dropbox/'$1'/'$2'/'$3 $homeSect

./findExtract.sh $homeSect
FILE="./DATA.enc"
tempFile="$FILE.txt"
TOKEN="dummy"
if [ ! -f $FILE ] 
then
 echo "Enter your canvas token:"
 read TOKEN
 echo $TOKEN > $tempFile
 openssl enc -e -aes-256-cbc -in $tempFile -out $FILE
 rm -rf $tempFile
else
 openssl enc -d -aes-256-cbc -in $FILE -out $tempFile
 TOKEN=`cat $tempFile`
 rm -rf $tempFile
fi
./callTK.sh $homeSect $2 $3 $TOKEN $homeClass
echo I should be the last one to show up!
