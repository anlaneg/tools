#! /bin/bash

function dummy_testcase()
{
	echo "just test"
	cmd="ls -l"
	$cmd
}

function udp_testcase()
{
	parallel="$1"
	cmd="timeout -s 9 65 iperf -u -c 8.8.8.8 -P $parallel -i 10 -p 9934 -t 60 -b 100G"
	echo "--------start udp testcase------"
	echo "$cmd"
	$cmd
	echo "--------end  udp testcase------"
}

function tcp_testcase()
{
	parallel="$1"
	cmd="iperf -c 8.8.8.8 -P $parallel -i 10 -p 9999 -t 60 -b 100G"
	echo "--------start tcp testcase------"
	echo "$cmd"
	$cmd
	echo "--------end tcp  testcase------"
}

function notice_server_prepare()
{
	protocol="$1"
	file="$2"
	python ./ptask.py client $protocol $file
}

function do_test()
{
	protocol="$1"
	paraller="$2"
	dir="$3"

	cmd="notice server prepare start"
	echo "$cmd"
	notice_server_prepare "$protocol" "${protocol}_${paraller}_flow.txt"	
	
	
	cmd="${protocol}_testcase $paraller > $dir/${protocol}_${paraller}_flow.txt"
	
	echo "$cmd"
	${protocol}_testcase $paraller > $dir/${protocol}_${paraller}_flow.txt
	echo "wait 5s"
	sleep 5
	cmd="notice server stop"
	echo "$cmd"
	notice_server_prepare "$protocol" 
}

function execute_testcase()
{
	dir="$1"
	protocol="$2"

	date
	do_test "$protocol" 1 "$dir"
	date
	do_test "$protocol" 5 "$dir"
	date
	do_test "$protocol" 10 "$dir"
	date
	do_test "$protocol" 20 "$dir"
	date
	do_test "$protocol" 50 "$dir"
	date
	do_test "$protocol" 100 "$dir"
}


function main()
{
	#execute_testcase "/root/result" "dummy"
	execute_testcase "/root/result" "udp"
	execute_testcase "/root/result" "tcp"
}

main
