#!/bin/sh
#
#
#PBS -N quast
#PBS -o result/output.txt
#PBS -e result/error.txt
#PBS -l walltime=03:59:00
#PBS -m n
#PBS -l nodes=1:ppn=1
#PBS -l vmem=12
cd /home/mahdi/autoScripts

./run_quast.sh "DIR" "Assembler"

