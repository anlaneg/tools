CONFIG_ALTERA_PCIE_CHDMA=m
prvpci-m=ourpci.o
obj-$(CONFIG_ALTERA_PCIE_CHDMA)	+= altpciechdma.o
obj-m += prvpci.o

KERNELDIR := /usr/src/linux-headers-`uname -r`

PWD := $(shell pwd)
default:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules
clean:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) clean

