#!/bin/bash

## test

cd ../raw_data

for i in {0..264};
do
	mkdir -p ${i}
	for file in *.json;
	do
		python3 preprocess.py ${file} ${i}
	done

	mv *_processed.csv ${i}/
	cd ${i}
	mv 202106_processed.csv ../station_${i}.csv
	awk FNR-1 * >> ../station_${i}.csv
	cd ..
	mv station_${i}.csv three_years/

done
