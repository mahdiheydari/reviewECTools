#cat ../initialContigsTop10.fasta | sed -n '/>NODE_3_/,/>NODE_4_/p' |head -n -1 >>$analisesDirRoot"NODE_3.fasta"
#jellyfish count -m 21 -o 21_reads_jellyfish" -c 3 -s 100000000 -t 64 reads.fastq
#jellyfish count -m 31 -o 31_reads_jellyfish" -c 3 -s 100000000 -t 64 reads.fastq
kmers=(21 31)
#methods=(ace racer musket bless blue fiona lighter sga bayesHammer trowel bfc)
#methods=(musket)
contigs=(2 1 3)
minLen=250

#for method in ${methods[@]}
#do
  method=$1
  analisesDir=$method   
  #rm $analisesDir/*
  for contig in ${contigs[@]}
  do
     
     minLen=250
     /home/mahdi/bin/MUMmer3.23/mummer -mum -b -c -l $minLen "NODE_"$contig".fasta" ../$method/"asm_spades_"$method/contigs.fasta| grep "^[^>]" -B 1 |sed '/^--/ d' >$method/$method"_sum_mummer_node"$contig"_"$minLen".mum"
     /home/mahdi/bin/MUMmer3.23/mummer -mum -b -c -l $minLen "NODE_"$contig".fasta" ../$method/"asm_spades_"$method/contigs.fasta >$method/$method"_mummer_node"$contig"_"$minLen".mum"
     /home/mahdi/bin/MUMmer3.23/mummerplot  -t png -p $method/$method"_mummer_node"$contig"_"$minLen".mum" $method/$method"_mummer_node"$contig"_"$minLen".mum"
 
   #jellyfish count -m 21 -o $analisesDir/21_lostKmer_jellyfish -c 3 -s 100000000 -t 64 ../$method/lostTrueKmer.fasta
   jellyfish count -m 21 -o $analisesDir/21_lostKmer_initialContig_jellyfish -c 3 -s 100000000 -t 64 ../$method/lostTrueKmer_initialContig.fasta
   for kmer in ${kmers[@]}
   do
     if [ $contig -eq "1" ];
     then
        echo "finding kmer around breakpoint in the first contig"
       	if [ $kmer -eq "21" ];
        then
        	python extractLostTrueKmerPos.py NODE_1.fasta $analisesDir/21_lostKmer_initialContig_jellyfish "../"$kmer"_reads_jellyfish" $analisesDir/alignment_1.dat $analisesDir/$kmer"_1_all_result".txt $kmer $analisesDir"/reads/"$contig $analisesDir/$method"_sum_mummer_node1_250.mum" true
        fi
        python extractLostTrueKmerPos.py NODE_1.fasta $analisesDir/21_lostKmer_initialContig_jellyfish "../"$kmer"_reads_jellyfish" $analisesDir/alignment_1.dat $analisesDir/$kmer"_1_result".txt $kmer $analisesDir"/reads/"$contig $analisesDir/$method"_sum_mummer_node1_250.mum" false
     fi
     if [ $contig -eq "2" ];
     then
        echo "finding kmer around breakpoint in the second contig"
     	if [ $kmer -eq "21" ];
        then
        	python extractLostTrueKmerPos.py NODE_2.fasta $analisesDir/21_lostKmer_initialContig_jellyfish "../"$kmer"_reads_jellyfish" $analisesDir/alignment_2.dat $analisesDir/$kmer"_2_all_result".txt $kmer $analisesDir"/reads/"$contig $analisesDir/$method"_sum_mummer_node2_250.mum" true
        fi
        python extractLostTrueKmerPos.py NODE_2.fasta $analisesDir/21_lostKmer_initialContig_jellyfish "../"$kmer"_reads_jellyfish" $analisesDir/alignment_2.dat $analisesDir/$kmer"_2_result".txt $kmer $analisesDir"/reads/"$contig $analisesDir/$method"_sum_mummer_node2_250.mum" false
     fi
     if [ $contig -eq "3" ];
     then
        echo "finding kmer around breakpoint in the third contig"
     	if [ $kmer -eq "21" ];
        then
        	python extractLostTrueKmerPos.py NODE_3.fasta $analisesDir/21_lostKmer_initialContig_jellyfish "../"$kmer"_reads_jellyfish" $analisesDir/alignment_3.dat $analisesDir/$kmer"_3_all_result".txt $kmer $analisesDir"/reads/"$contig $analisesDir/$method"_sum_mummer_node3_250.mum" true
        fi 
       python extractLostTrueKmerPos.py NODE_3.fasta $analisesDir/21_lostKmer_initialContig_jellyfish "../"$kmer"_reads_jellyfish" $analisesDir/alignment_3.dat $analisesDir/$kmer"_3_result".txt $kmer $analisesDir"/reads/"$contig $analisesDir/$method"_sum_mummer_node3_250.mum" false
     fi
   done
 done
#done

#./extractReads.sh ace 1 
#./extractReads.sh ace 2 &
#./extractReads.sh racer 1 &
#./extractReads.sh racer 2 &
#./extractReads.sh musket 1 &
#./extractReads.sh musket 2
#./extractReads.sh karect 2
#./extractReads.sh racer &
#./extractReads.sh ace &
#./extractReads.sh bless &
#./extractReads.sh musket &
#./extractReads.sh blue 
#./extractReads.sh fiona &
#./extractReads.sh lighter &
#./extractReads.sh sga &
#./extractReads.sh bayesHammer &
#./extractReads.sh trowel &
#./extractReads.sh bfc &

