CONFIG_ALTERA_PCIE_CHDMA=m
obj-$(CONFIG_ALTERA_PCIE_CHDMA)	+= altpciechdma.o
KERNELDIR := /usr/src/linux-headers-`uname -r`

PWD := $(shell pwd)
default:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules
clean:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) clean

