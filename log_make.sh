echo "$ make clean clean_assets clean_baserom"
make clean clean_assets clean_baserom

echo ""
echo "$ python3 extract_baserom.py $1"
python3 extract_baserom.py $1 > logs/log_extract_baserom_$1.txt 2>&1

echo ""
echo "$ python3 extract_assets.py"
python3 extract_assets.py > logs/log_extract_assets_$1.txt 2>&1

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt > logs/log_compare_extracted_baseroms_$1_vs_pal_mq_dbg.txt
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --csv > logs/log_compare_extracted_baseroms_$1_vs_pal_mq_dbg.csv

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print equals"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print equals > logs/log_compare_extracted_baseroms_equals_$1_vs_pal_mq_dbg.txt
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print equals --csv > logs/log_compare_extracted_baseroms_equals_$1_vs_pal_mq_dbg.csv

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print diffs"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print diffs > logs/log_compare_extracted_baseroms_diffs_$1_vs_pal_mq_dbg.txt
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print diffs --csv > logs/log_compare_extracted_baseroms_diffs_$1_vs_pal_mq_dbg.csv

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print missing"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print missing > logs/log_compare_extracted_baseroms_missing_$1_vs_pal_mq_dbg.txt
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom filelists/filelist_pal_mq_dbg.txt --print missing --csv > logs/log_compare_extracted_baseroms_missing_$1_vs_pal_mq_dbg.csv

echo ""
echo "$ make all"
make all > logs/log_make_all_$1.txt 2>&1

echo ""
echo "Logs done."
