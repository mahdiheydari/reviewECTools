#!/bin/sh
i=0
j=0
array=()
while IFS='' read -r line || [[ -n "$line" ]]; do
    
    let "i += 1"
    for word in $line
    do
        let "j += 1"
        if ! ((j % 2)); then
         if [ "${word}" != "0" ]
         then
          let array[word]++
         fi
        fi
    done
    #if [ $i -gt 20000 ]
    #then
    #  break
    #fi
done < "$1"
#echo "${array[@]}"
for index in "${!array[@]}"
do
    echo "$index ${array[index]}"
done
 
