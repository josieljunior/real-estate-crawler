#!/bin/bash

pages_to_crawl=$1
nome_do_crawler=$2

docker-compose run --rm scrapy /bin/bash -c "cd real_estate_crawler/real_estate_crawler/ && scrapy crawl $nome_do_crawler -a pages_to_crawl=$pages_to_crawl"
