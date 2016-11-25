#scp -r mahdi@halo.intec.ugent.be:/home/share/data/mahdi/illumina/D8/aceAnalises/test.tar.gz ace/ace.tar.gz
methods=(musket blue fiona lighter bayesHammer trowel)
#methods=(karect)
for method in ${methods[@]}
do
#rm -rf $method/*
scp -r mahdi@halo.intec.ugent.be:/home/share/data/mahdi/illumina/D8/$method"Analises"/$method".tar.gz" $method/$method".tar.gz"
cd $method
echo "we are in the " $method " folder"
tar xvzf $method".tar.gz"
cat  21_result.txt | sed -n '/NODE_3_/,/NODE_4_/p' |head -n -1 >21_3.fasta
cat  21_result.txt | sed -n '/NODE_2_/,/NODE_3_/p' |head -n -1 >21_2.fasta
cat  21_result.txt | sed -n '/NODE_1_/,/NODE_2_/p' |head -n -1 >21_1.fasta


cat  31_result.txt | sed -n '/NODE_3_/,/NODE_4_/p' |head -n -1 >31_3.fasta
cat  31_result.txt | sed -n '/NODE_2_/,/NODE_3_/p' |head -n -1 >31_2.fasta
cat  31_result.txt | sed -n '/NODE_1_/,/NODE_2_/p' |head -n -1 >31_1.fasta

plotName="../breakpoint.dem"


a="21_1.fasta"
b="31_1.fasta"
c=$method"_1.pdf"
gnuplot -e "inputFilename21='$a'"  -e "inputFilename31='$b'" -e "outputFilename='$c'" -e "titleName='$method'" $plotName 


a="21_2.fasta"
b="31_2.fasta"
c=$method"_2.pdf"
gnuplot -e "inputFilename21='$a'"  -e "inputFilename31='$b'" -e "outputFilename='$c'" -e "titleName='$method'" $plotName 

a="21_3.fasta"
b="31_3.fasta"
c=$method"_3.pdf"
gnuplot -e "inputFilename21='$a'"  -e "inputFilename31='$b'" -e "outputFilename='$c'" -e "titleName='$method'" $plotName 

cd ..
done
