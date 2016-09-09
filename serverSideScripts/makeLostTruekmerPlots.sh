




methods=(musket)

#methods=(ace bless blue bfc brownie initial karect racer fiona lighter sga bayesHammer trowel)

cd /home/share/data/mahdi/illumina

    cd D8
    kmer=21
    for m in ${methods[@]}
    do
        lostTrueKmerFreq=$m"Out"/$m"lostTrueKmerFreq"$kmer".dat"
        lostTrueKmer=$m"Out"/$m"lostTrueKmer"$kmer
        echo $lostTrueKmerFreq
        echo $lostTrueKmer
        cd $m
        jellyfish query ../mer_counts_21.jf -s lostTrueKmer.fasta >$lostTrueKmer        
        ../extractKmerFreq.sh $lostTrueKmer >$lostTrueKmerFreq 
        cd ..
    done

