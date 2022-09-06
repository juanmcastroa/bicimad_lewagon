#!/bin/bash

## test


for i in {0..264};
do

	for file in *.json;
	do
		python3 preprocess.py ${file} ${i}
	done
	cd ../raw_data
  mkdir -p ${i}
	mv *_processed.csv ${i}/
	cd ${i}
	mv 202106_processed.csv ../station_${i}.csv
	awk FNR-1 * >> ../station_${i}.csv
	cd ..
	mv station_${i}.csv three_years/
  cd ../scripts
done
