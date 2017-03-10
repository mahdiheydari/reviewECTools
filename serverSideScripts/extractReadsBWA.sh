
     method=$1
     contigNum=$2
     start=$3 
     length=$4
     echo $start
     echo $length 
     analisesDir=$method"/reads/"$contigNum"/C_"$contigNum"_"$start"/"
     mkdir -p $analisesDir
     rm  -rf  $analisesDir/*     
     mkdir -p $analisesDir"/reference"

     python extractReadsFromSam.py $start $length "../sorted"$contigNum"_.sam" ../reads100.fastq ../$method/$method"Out/checked."$method"Corrected.fastq" $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq

     if [ $contigNum -eq "1" ];
     then
        cat ../initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_1_/,/>NODE_2_/p' |head -n -1 >$analisesDir"reference/1_contig.fasta"
     fi

    if [ $contigNum -eq "2" ];
     then
      cat ../initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_2_/,/>NODE_3_/p' |head -n -1 >$analisesDir"reference/2_contig.fasta"
    fi

    if [ $contigNum -eq "3" ];
     then
      cat ../initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_3_/,/>NODE_4_/p' |head -n -1 >$analisesDir"reference/3_contig.fasta"
     fi


     bwa index $analisesDir/reference/$contigNum"_contig.fasta"
     bwa mem -M -t 4 $analisesDir/reference/$contigNum"_contig.fasta" $analisesDir"mapped.fastq" | samtools view  -Sb - | samtools sort - $analisesDir"sorted" && samtools index $analisesDir"sorted.bam"
     samtools view $analisesDir"/sorted.bam" > $analisesDir"/sorted.sam"
     python alignmentSVG/alignmentSVG.py $analisesDir"reference/"$contigNum"_contig.fasta" $start $length $analisesDir"/sorted.sam" $analisesDir"mapped.fastq" $analisesDir/mappedCorrected.fastq > $analisesDir$start"output.svg"








