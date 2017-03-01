#! /bin/bash

source ./build-env

OVS_PATH="$MY_OVS_BUILD_ROOT/anlaneg_ovs:$MY_OVS_BUILD_ROOT/anlaneg_ovs/utilities:$MY_OVS_BUILD_ROOT/anlaneg_ovs/ovsdb:\
$MY_OVS_BUILD_ROOT/anlaneg_ovs/vswitchd:$MY_OVS_BUILD_ROOT/anlaneg_ovs/vtep"
#echo "---$OVS_PATH---"
export PATH=$PATH:$OVS_PATH
function set_hugepages()
{
    sysctl -w vm.nr_hugepages=512

    mount | grep -q "hugetlbfs on /dev/hugepages"
    if [ ! "$?" == "0" ];
    then
        mkdir -p /dev/hugepages
	mount -t hugetlbfs none /dev/hugepages
    else
        echo "mount already"
    fi;
}

function config_dpdk()
{
   modprobe uio
   insmod igb_uio
}

function config_ovs()
{
   echo "$PATH"
    
    mkdir -p /usr/local/etc/openvswitch
    mkdir -p /usr/local/var/run/openvswitch
    mkdir -p /usr/local/var/log/openvswitch/
    ovsdb-tool create /usr/local/etc/openvswitch/conf.db $MY_OVS_BUILD_ROOT/anlaneg_ovs/vswitchd/vswitch.ovsschema
    ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
     --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
     --private-key=db:Open_vSwitch,SSL,private_key \
     --certificate=db:Open_vSwitch,SSL,certificate \
     --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
     --pidfile --detach --log-file
    ovs-vsctl --no-wait init 
    ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true
    ovs-vsctl --no-wait set Open_vSwitch . other_config:log-level=9
    ovs-vswitchd --pidfile --detach --log-file
}

function ovs_test()
{
    ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
    #need unbind from kernel
    #
    #./dpdk-devbind.py --status
    #./dpdk-devbind.py -b igb_uio 02:03.0
    #ls  -al /sys/class/net
    ovs-vsctl add-port br0 myportnameone -- set Interface myportnameone \
          type=dpdk options:dpdk-devargs=0000:02:02.0
    ovs-vsctl add-port br0 myportnametwo -- set Interface myportnametwo \
          type=dpdk options:dpdk-devargs=0000:02:03.0
}

set_hugepages
config_ovs
