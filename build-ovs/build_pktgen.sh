#!/bin/bash

export DPDK_BASE_DIR=`pwd`
export DPDK_VERSION=dpdk-16.11
export DPDK_TARGET=x86_64-native-linuxapp-gcc
#export DPDK_BUILD=$DPDK_BASE_DIR/$DPDK_VERSION/$DPDK_TARGET
export PKTGEN=pktgen-dpdk-pktgen-3.0.17
export RTE_SDK='/home/dpdk'

echo "Cleaning.."
if [ -d "$DPDK_BASE_DIR/$PKTGEN" ]; then
  rm -rf $DPDK_BASE_DIR/$PKTGEN
fi

if [ ! -e "$DPDK_BASE_DIR/$PKTGEN.tar.gz" ]; then
  echo "Downloading.."
  wget http://dpdk.org/browse/apps/pktgen-dpdk/snapshot/$PKTGEN.tar.gz --directory-prefix=$DPDK_BASE_DIR
fi

echo "Extracting.."
tar xf $DPDK_BASE_DIR/$PKTGEN.tar.gz -C $DPDK_BASE_DIR
cd $DPDK_BASE_DIR/$PKTGEN
make RTE_SDK=$RTE_SDK RTE_TARGET=$DPDK_TARGET

ln -s $DPDK_BASE_DIR/$PKTGEN/app/app/x86_64-native-linuxapp-gcc/pktgen $DPDK_BASE_DIR/dpdk-pktgen

~     
