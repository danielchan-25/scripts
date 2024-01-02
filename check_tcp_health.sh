#!/bin/sh
# ------------------------------- #
# 日期：2024年1月2日
# 作者：陈某
# 说明：检测网络端口是否阻塞
# ------------------------------- #
tcp_status=$(netstat -tnlp | awk '!/Internet|Recv-Q/ {print $2}')

if [[ $tcp_status =~ 0 ]]; then
  echo "未检测到网络端口阻塞"
else
	echo "检测到网络端口阻塞!!"
fi
