#!/bin/tcsh

#$ -N Nomi
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU
#$ -q comp7.itaym.q@compute-7-0.loc

python ./my.py
