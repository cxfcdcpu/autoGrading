#!/bin/sh
location=$7
homeDir=$7'/'$6
homeSect=$7'/'$6'/'$4'/'
echo $homeDir
./changeDir.sh $homeDir $homeSect
./sftpExpect.sh $1 $2 $3 $homeSect $4 $5 $6
./findExtract.sh $homeSect$5
./callTK.sh $homeSect$5 $4 $5
