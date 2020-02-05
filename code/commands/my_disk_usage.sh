#!/bin/tcsh

#$ -N du_analysis
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU

eval echo ~$USER | du -h --max-depth=1 > my_disk_usage.txt
# du -h ~/EcoGeo/ --max-depth=2 > ~/my_disk_usage.txt &
