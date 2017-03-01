#! /bin/bash

source ./build-env

function git_checkout()
{
    url="$1"
    dir="$MY_OVS_BUILD_ROOT/$2"
    if [ ! -e $dir ];
    then
        git clone $url $dir
    else
        (echo "try update $dir";cd $dir ; git pull);
    fi;
}

function checkout_project()
{
    git_checkout 'https://github.com/anlaneg/ovs.git' anlaneg_ovs
    git_checkout 'https://github.com/anlaneg/dpdk.git' anlaneg_dpdk
    git_checkout 'https://github.com/anlaneg/qemu.git' anlaneg_qemu
}

function compile_dpdk()
{
    export DPDK_DIR="$MY_OVS_BUILD_ROOT/anlaneg_dpdk"
    export DPDK_TARGET='x86_64-native-linuxapp-gcc'
    export DPDK_BUILD="$DPDK_DIR/$DPDK_TARGET"
    (echo "compile dpdk";cd $DPDK_DIR;make EXTRA_CFLAGS="-O0 -g" install T=$DPDK_TARGET DESTDIR=install);
}

function compile_ovs()
{
    export OVS_DIR="$MY_OVS_BUILD_ROOT/anlaneg_ovs"
    (echo 'compile ovs';cd $OVS_DIR;./boot.sh;./configure --with-dpdk=$DPDK_BUILD --with-debug  CFLAGS='-g' ; make -j4 1>/dev/null);
}

function compile_qemu()
{
    export QEMU_DIR="$MY_OVS_BUILD_ROOT/anlaneg_qemu"
    (echo 'compile qemu';cd $QEMU_DIR;rm -rf bin; mkdir bin ; cd bin ; ../configure --target-list=x86_64-softmmu --enable-debug --extra-cflags='-g'; make -j4 )
}

checkout_project
compile_dpdk
compile_ovs
compile_qemu
