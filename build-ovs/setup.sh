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
    #ovs-vsctl add-port br0 myportnameone -- set Interface myportnameone \
    #      type=dpdk options:dpdk-devargs=0000:02:02.0
    #ovs-vsctl add-port br0 myportnametwo -- set Interface myportnametwo \
    #      type=dpdk options:dpdk-devargs=0000:02:03.0
    ovs-vsctl add-port br0 vhost-user1 -- set Interface vhost-user1 type=dpdkvhostuser
}

function download_image()
{
    resource_dir="$MY_OVS_BUILD_ROOT/anlaneg_resource"
    mkdir -p "$resource_dir"
    if [ ! -e "$resource_dir/cirros-0.3.5-x86_64-disk.img" ];
    then
        wget -c http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img -O $resource_dir/cirros-0.3.5-x86_64-disk.img ;
    fi;
}

function qemu_config()
{
    ovs-vsctl add-port br0 vhost-user1 -- set Interface vhost-user1 type=dpdkvhostuser
    ovs-vsctl add-port br0 vhost-user2 -- set Interface vhost-user2 type=dpdkvhostuser
}

function setup_vm()
{
./qemu-system-x86_64 -enable-kvm -m 1024 -smp 2     -chardev socket,id=char0,path=/usr/local/var/run/openvswitch/vhost-user1     -netdev type=vhost-user,id=mynet1,chardev=char0,vhostforce     -device virtio-net-pci,netdev=mynet1,mac=52:54:00:02:d9:01     -object memory-backend-file,id=mem,size=1024M,mem-path=/dev/hugepages,share=on     -numa node,memdev=mem -mem-prealloc     -net user,hostfwd=tcp::10021-:22 -net nic   /home/along/project/anlaneg_resource/cirros-0.3.5-x86_64-disk.img
}



set_hugepages
config_ovs
download_image
