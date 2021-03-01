echo "$ make clean clean_assets clean_baserom"
make clean clean_assets clean_baserom

echo ""
echo "$ python3 extract_baserom.py pal_mq"
python3 extract_baserom.py pal_mq > logs/log_extract_baserom_pal_mq.txt 2>&1

echo ""
echo "$ python3 extract_assets.py"
python3 extract_assets.py > logs/log_extract_assets_pal_mq.txt 2>&1

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom > logs/log_compare_extracted_baseroms_pal_mq_vs_pal_mq_dbg.txt 2>&1
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --csv > logs/log_compare_extracted_baseroms_pal_mq_vs_pal_mq_dbg.csv

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print equals"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print equals > logs/log_compare_extracted_baseroms_equals_pal_mq_vs_pal_mq_dbg.txt 2>&1
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print equals --csv > logs/log_compare_extracted_baseroms_equals_pal_mq_vs_pal_mq_dbg.csv

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print diffs"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print diffs > logs/log_compare_extracted_baseroms_diffs_pal_mq_vs_pal_mq_dbg.txt 2>&1
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print diffs --csv > logs/log_compare_extracted_baseroms_diffs_pal_mq_vs_pal_mq_dbg.csv

echo ""
echo "$ python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print missing"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print missing > logs/log_compare_extracted_baseroms_missing_pal_mq_vs_pal_mq_dbg.txt 2>&1
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom --print missing --csv > logs/log_compare_extracted_baseroms_missing_pal_mq_vs_pal_mq_dbg.csv

echo ""
echo "$ make all"
make all > logs/log_make_all_pal_mq.txt 2>&1

echo ""
echo "Logs done."
