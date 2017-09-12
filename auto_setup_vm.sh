#! /bin/bash
#"lenovo-roller" {b1396ab1-9271-42c4-974e-8705171cb735}
#"lenovo-zabbix" {86bce432-10fd-464d-82dc-b60b12855dd7}
#"lenovo-ceph-mgmt" {4bfd78f1-bd8b-4b49-a002-4a37b5dd4b47}
#"lenovo lxca" {59f4b313-3dda-4383-a4b9-3db18abcd529}
zabbix_name="lenovo-zabbix"
all_vms=(
"lenovo-roller"
"lenovo-ceph-mgmt"
"lenovo lxca" 
"$zabbix_name"  # zabbix must last one
)

function start_vm()
{
	vmname="$1"
	echo "start vm $1"
	if [ "$2" != "0" ];then
		echo "lazy $2"
		sleep $2
	fi;
	echo "setup"
	vboxheadless --startvm "$vmname" --vrde on  &
}

function stop_vm()
{
	vmname="$1"
	echo "stop vm $1"
	vboxmanage controlvm  "$vmname" poweroff
}

function controller_vms()
{
	vms_count=${#all_vms[@]}
	for((i=0;i<$vms_count;++i))
	do
		echo "$1 \"${all_vms[$i]}\""
		if [ $1 == "start" ]; then
			lazy_time="0"
			if [ "${all_vms[$i]}" == "$zabbix_name" ]; then
				lazy_time="120"
			fi;
			start_vm "${all_vms[$i]}" "$lazy_time";
		elif [ $1 == "stop" ] ; then
		    stop_vm "${all_vms[$i]}";
	        else
		    echo "unkown command";
		fi;
	done; 
}

if [ $1 == "stop" ]; then
	controller_vms "$1"
elif [ $1 == "start" ] ; then
	controller_vms "$1"
else
	echo "unkown command"
fi;
