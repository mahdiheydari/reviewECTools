      

        
       #bwa index reference/NODE_1.fasta
       #bwa mem -M -t 32 -p reference/NODE_1.fasta reads100.fastq | samtools view  -Sb - | samtools sort - sorted1 && samtools index sorted1.bam
       #samtools view sorted1.bam > sorted1_.sam

       bwa index reference/NODE_2.fasta
       bwa mem -M -t 32 -p reference/NODE_2.fasta ../reads100.fastq | samtools view  -Sb - | samtools sort - sorted2 && samtools index sorted2.bam
       samtools view sorted2.bam > sorted2_.sam
 
       #bwa index reference/NODE_3.fasta
       #bwa mem -M -t 32 -p reference/NODE_3.fasta reads100.fastq | samtools view  -Sb - | samtools sort - sorted3 && samtools index sorted3.bam
       #samtools view sorted3.bam > sorted3_.sam

