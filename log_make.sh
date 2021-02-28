echo "> make clean clean_assets"
make clean clean_assets

echo ""
echo "> python3 extract_baserom.py > logs/log_extract_baserom_pal_mq.txt 2>&1"
python3 extract_baserom.py > logs/log_extract_baserom_pal_mq.txt 2>&1

echo ""
echo "> python3 extract_assets.py > logs/log_extract_assets_pal_mq.txt 2>&1"
python3 extract_assets.py > logs/log_extract_assets_pal_mq.txt 2>&1

echo ""
echo "> python3 tools/compare_extracted_baseroms.py ../oot_master/baserom > logs/log_compare_extracted_baseroms_pal_mq_vs_pal_mq_dbg.txt 2>&1"
python3 tools/compare_extracted_baseroms.py ../oot_master/baserom > logs/log_compare_extracted_baseroms_pal_mq_vs_pal_mq_dbg.txt 2>&1

echo ""
echo "> make all > logs/log_make_all_pal_mq.txt 2>&1"
make all > logs/log_make_all_pal_mq.txt 2>&1

echo ""
echo "Logs done."
