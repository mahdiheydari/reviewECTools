methods=(ace bfc bless blue karect racer sga musket blue fiona lighter bayesHammer trowel)
#methods=(blue)
for method in ${methods[@]}
do
rm $method/*
scp -r  mahdi@halo.intec.ugent.be:/home/share/data/mahdi/illumina/D8/fragmentationAnalysis/$method/* $method/
done

#scp -r  mahdi@halo.intec.ugent.be:/home/share/data/mahdi/illumina/D8/fragmentationAnalysis/* .

for method in ${methods[@]}
do


#we need the folloing segment only for the current data, later it would be fixed automaticly 
    mv $method/21_2_all_result.txt $method/21_2_result_temp.txt
    mv $method/21_2_result.txt $method/21_2_all_result.txt
    mv $method/21_2_result_temp.txt $method/21_2_result.txt

    mv $method/31_2_all_result.txt $method/31_2_result_temp.txt
    mv $method/31_2_result.txt $method/31_2_all_result.txt
    mv $method/31_2_result_temp.txt $method/31_2_result.txt

    mv $method/21_3_all_result.txt $method/21_3_result_temp.txt
    mv $method/21_3_result.txt $method/21_3_all_result.txt
    mv $method/21_3_result_temp.txt $method/21_3_result.txt

    mv $method/31_3_all_result.txt $method/31_3_result_temp.txt
    mv $method/31_3_result.txt $method/31_3_all_result.txt
    mv $method/31_3_result_temp.txt $method/31_3_result.txt


    python pythonScripts/removeNonezero.py $method/21_1_all_result.txt $method/21_1_sum.txt
    python pythonScripts/removeNonezero.py $method/21_2_all_result.txt $method/21_2_sum.txt
    python pythonScripts/removeNonezero.py $method/21_3_all_result.txt $method/21_3_sum.txt
    python pythonScripts/FindHighFrequnetKmers.py $method/21_1_all_result.txt $method/21_1_result_HighFrequentKmer.txt
    python pythonScripts/FindHighFrequnetKmers.py $method/21_2_all_result.txt $method/21_2_result_HighFrequentKmer.txt
done


#gnuplot breakpoint_1.dem
#gnuplot breakpoint_2.dem

