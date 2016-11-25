 
methods=(ace racer karect musket bless blue fiona lighter sga bayesHammer trowel bfc)
for method in ${methods[@]}
do  
    method=$1
    analisesDir=$method"Analises/reads/1/"
    rm $analisesDir/mapped.fastq
    rm $analisesDir/mappedCorrected.fastq 
    #python extractUniqueReads.py $analisesDir/41kmer_NODE_1_length_482029_cov_17.7599_ID_1072487 $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq reads.fastq $method/$method"Out/checked."$method"Corrected.fastq"
    python extractUniqueReads.py $analisesDir/21kmer_NODE_1_length_518285_cov_20.8169_ID_1059665 $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq reads.fastq karect/karectOut/checked.karectCorrected.fastq

    mkdir $analisesDir/reference
    cat initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_1_/,/>NODE_2_/p' |head -n -1 >$analisesDir/reference/1_contig.fasta
    bwa index $analisesDir/reference/1_contig.fasta
 bwa mem -M -t 4 -p $analisesDir/reference/1_contig.fasta $analisesDir/mapped.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sorted && samtools index $analisesDir/sorted.bam
 bwa mem -M -t 4 -p $analisesDir/reference/1_contig.fasta $analisesDir/mappedCorrected.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sortedCorr && samtools index $analisesDir/sortedCorr.bam
   
    analisesDir=$method"Analises/reads/2/"
    rm $analisesDir/mapped.fastq
    rm $analisesDir/mappedCorrected.fastq
    python extractUniqueReads.py $analisesDir/41kmer_NODE_2_length_405178_cov_15.7823_ID_1072511 $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq reads.fastq $method/$method"Out/checked."$method"Corrected.fastq"
    mkdir $analisesDir/reference
    cat initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_2_/,/>NODE_3_/p' |head -n -1 >$analisesDir/reference/2_contig.fasta
    bwa index $analisesDir/reference/2_contig.fasta
bwa mem -M -t 4 -p $analisesDir/reference/2_contig.fasta $analisesDir/mapped.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sorted && samtools index $analisesDir/sorted.bam
bwa mem -M -t 4 -p $analisesDir/reference/2_contig.fasta $analisesDir/mappedCorrected.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sortedCorr && samtools index $analisesDir/sortedCorr.bam


    analisesDir=$method"Analises/reads/3/"
    rm $analisesDir/mapped.fastq
    rm $analisesDir/mappedCorrected.fastq
    python extractUniqueReads.py $analisesDir/41kmer_NODE_3_length_378768_cov_17.4572_ID_1072515 $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq reads.fastq $method/$method"Out/checked."$method"Corrected.fastq"
    mkdir $analisesDir/reference
    cat initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_3_/,/>NODE_4_/p' |head -n -1 >$analisesDir/reference/3_contig.fasta
    bwa index $analisesDir/reference/3_contig.fasta
bwa mem -M -t 4 -p $analisesDir/reference/3_contig.fasta $analisesDir/mapped.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sorted && samtools index $analisesDir/sorted.bam
bwa mem -M -t 4 -p $analisesDir/reference/3_contig.fasta $analisesDir/mappedCorrected.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sortedCorr && samtools index $analisesDir/sortedCorr.bam

done