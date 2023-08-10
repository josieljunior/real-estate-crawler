#!/bin/bash

log_file="./backup.log"

backup_date=$(date +"%Y%m%d%H%M%S")

backup_path="./db_backup/$backup_date.sql"

docker exec e7af3718fc5d /usr/bin/mysqldump -u root -psecret real_estate_crawler > $backup_path

gsutil cp $backup_path gs://crawler_backup/ >> $log_file 2>&1

echo "-----------------------------------------------" >> $log_file

