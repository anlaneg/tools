#! /bin/bash

BR="NONE"
function alongdump_prepare_tcpdump()
{
	alongdump_finish_tcpdump
	BR="$1"
	port="$2"

	ovs-vsctl add-port $BR tap0 -- set Interface tap0 type=tap
	ovs-vsctl  \
	-- --id=@dst get port tap0 \
	-- --id=@src get port $port \
	-- --id=@m create mirror name=m0 \
	select-dst-port=@src \
	select-src-port=@src \
	output-port=@dst    -- set bridge $BR mirrors=@m
	ifconfig tap0 up
	
}

function alongdump_finish_tcpdump()
{
	if [ "X$BR" != "XNONE" ];
	then
		ovs-vsctl del-port $BR tap0
		ovs-vsctl clear bridge $BR mirrors
		BR=NONE
	fi;
}

