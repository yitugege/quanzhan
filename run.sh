#!/bin/sh
source /home/yitu/tutorial-env/bin/activate
#dir1=`cd /home/yitu/quanzhan/mercado_redis/spiders/`
#dir2=`cd /home/yitu/scrapy-redis/scrapy_redis_test/spiders/`
#command=`nohup python -u run.py > 1.log 2>&1 &`
quanzhan_pid=`ps -aux|grep -v 'grep'|grep -c 'quanzhan'`
mercado_pid=`ps -aux|grep -v 'grep'|grep -c 'mercado'`
if [ $quanzhan_pid -eq 0 ]
then
  cd /home/yitu/quanzhan
  pull
  cd /home/yitu/quanzhan/mercado_redis/spiders/
  nohup python -u run.py > 1.log 2>&1 &
fi

if [ $mercado_pid -eq 0 ]
then
  cd /home/yitu/scrapy-redis/
  pull 
  cd /home/yitu/scrapy-redis/scrapy_redis_test/spiders/
  nohup python -u run.py > 1.log 2>&1 &
fi


