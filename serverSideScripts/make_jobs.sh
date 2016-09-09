
#!/bin/sh
#
#

methods=(ace bless blue brownie initial karect racer fiona lighter sga bayesHammer trowel bfc)
assembler=(velvet minia idba spades discovar)

current=${PWD}
jobFolder=jobs/ErrorCorrection

cd /home/share/data/mahdi/
i=0                   # Integer.
for directory in `find  ./illumina  -maxdepth 1 -mindepth 1   -type d `
   do
    #arr[i]=$directory
    arr[i]=$( echo $directory | cut -d "." -f 2 )
    let "i += 1"
    echo $directory
done

cd $current
mkdir -p jobs
rm -fr jobs/*
cd jobs
mkdir ErrorCorrection
mkdir Assembler
mkdir Quast
cd $current

for m in ${methods[@]}
do
  mkdir -p $jobFolder/result
  mkdir -p $jobFolder/$m
  j=0
  mkdir -p $jobFolder/$m/result
  for i in "${arr[@]}"
    do
      
      let "j += 1"
      first='/'
      second='\/'
      a=${i//$first/$second}
      ##replace directory      
      sed "s/DIR/$a/g" job_errorCorrection.sh > $jobFolder/$m/errorCorrection_oejob$j.sh
      sed "s/errorCorrection.output.txt/errorCorrection.output$j.txt/g" $jobFolder/$m/errorCorrection_oejob$j.sh>$jobFolder/$m/errorCorrection_ejob$j.sh
      sed "s/errorCorrection.error.txt/errorCorrection.error$j.txt/g" $jobFolder/$m/errorCorrection_ejob$j.sh>$jobFolder/$m/errorCorrection_job$j.sh
      rm $jobFolder/$m/errorCorrection_oejob$j.sh
      rm $jobFolder/$m/errorCorrection_ejob$j.sh
      ##replace toolname
      sed "s/ECTool/$m/g" $jobFolder/$m/errorCorrection_job$j.sh > $jobFolder/$m/$m'_'$j.sh
      rm $jobFolder/$m/errorCorrection_job$j.sh
      for s in ${assembler[@]}
      do
        echo "#nohup ./run_asembler.sh \""$i"\" "$m" "$s "2>&1  &">> $jobFolder/$m/$m'_'$j.sh
      done
      chmod u+x $jobFolder/$m/$m'_'$j.sh 
      
      #echo "nohup ./"$m"/"$m'_'$j.sh ">>"$m"/result/"$m".output"$j".txt >>"$m"/result/"$m".error"$j".txt 2>&1  &" >>$jobFolder/$m/runJobsInSeq.sh      
      echo "./"$m"/"$m'_'$j.sh ">>"$m"/result/"$m".output"$j".txt >>"$m"/result/"$m".error"$j".txt 2>&1 " >>$jobFolder/$m/runJobsInSeq.sh

      chmod u+x $jobFolder/$m/runJobsInSeq.sh
  done
  echo "nohup ./"$m/runJobsInSeq.sh ">>result/output.txt >>result/error.txt 2>&1  &" >> $jobFolder/runJobsInPar.sh 
  chmod u+x $jobFolder/runJobsInPar.sh
done 
 
jobFolder=jobs/Assembler

for  m in ${methods[@]} 
do
    mkdir -p $jobFolder/$m
    for s in ${assembler[@]}
    do
	mkdir -p $jobFolder/$m/$s
	j=0
	for i in "${arr[@]}"
	do
	    let "j += 1"
	    first='/'
	    second='\/'
	    a=${i//$first/$second}
	    ##replace directory      
	    sed "s/DIR/$a/g" job_assembler.sh > $jobFolder/$m/$s/job_assembler_oejob$j.sh
	    sed "s/job_assembler.output.txt/job_assembler.output$j.txt/g" $jobFolder/$m/$s/job_assembler_oejob$j.sh>$jobFolder/$m/$s/job_assembler_ejob$j.sh
	    sed "s/job_assembler.error.txt/job_assembler.error$j.txt/g" $jobFolder/$m/$s/job_assembler_ejob$j.sh>$jobFolder/$m/$s/job_assembler_job$j.sh
	    rm $jobFolder/$m/$s/job_assembler_oejob$j.sh
	    rm $jobFolder/$m/$s/job_assembler_ejob$j.sh
	    ##replace toolname
	    sed "s/ECTool/$m/g" $jobFolder/$m/$s/job_assembler_job$j.sh > $jobFolder/$m/$s/$m'_'$j.sh
	    rm $jobFolder/$m/$s/job_assembler_job$j.sh 
	    sed "s/Assembler/$s/g" $jobFolder/$m/$s/$m'_'$j.sh > $jobFolder/$m/$s/$m'_'$s'_'$j.sh
	    rm $jobFolder/$m/$s/$m'_'$j.sh


            echo "./"$m'_'$s'_'$j".sh>>result/output"$j".txt >>result/error"$j".txt " >>  $jobFolder/$m/$s/runJobsInSeq.sh
            chmod u+x $jobFolder/$m/$s/$m'_'$s'_'$j.sh

	    
	done
    done 
done

jobFolder=jobs/Quast

    for s in ${assembler[@]}
    do
        mkdir -p $jobFolder/$s
        mkdir -p $jobFolder/$s/result
        j=0
        for i in "${arr[@]}"
        do
            let "j += 1"
            first='/'
            second='\/'
            a=${i//$first/$second}
            ##replace directory
            sed "s/DIR/$a/g" job_quast.sh > $jobFolder/$s/job_quast_oejob$j.sh
            sed "s/job_quast.output.txt/job_quast.output$j.txt/g" $jobFolder/$s/job_quast_oejob$j.sh>$jobFolder/$s/job_quast_ejob$j.sh
            sed "s/job_quast.error.txt/job_quast.error$j.txt/g" $jobFolder/$s/job_quast_ejob$j.sh>$jobFolder/$s/job_quast_job$j.sh
            rm $jobFolder/$s/job_quast_oejob$j.sh
            rm $jobFolder/$s/job_quast_ejob$j.sh
            sed "s/Assembler/$s/g" $jobFolder/$s/job_quast_job$j.sh > $jobFolder/$s/$s'_'$j.sh
            rm $jobFolder/$s/job_quast_job$j.sh
            echo "nohup" $s'_'$j.sh ">>result/output"$j".txt >>result/error"$j".txt 2>&1  &" >>  $jobFolder/$s/runJobsInPar.sh
            chmod u+x $jobFolder/$s/$s'_'$j.sh
        done
    done

