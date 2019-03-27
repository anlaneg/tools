/*
 * ourpci.c
 *
 *  Created on: Jul 9, 2018
 *      Author: anlang
 */

#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/delay.h>
#include <linux/dma-mapping.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/io.h>
#include <linux/jiffies.h>
#include <linux/module.h>
#include <linux/pci.h>

#define __devinit
#define __devexit
#define __devexit_p(p) p
#define __DATE__ "2018-XX-XX"
#define __TIME__ "00:00:00"
#define DRV_NAME "altpciechdma"

static const struct pci_device_id ids[] = {
	{ PCI_DEVICE(0x1172, 0xE001), },
	{ PCI_DEVICE(0x2071, 0x2071), },
	{ 0, }
};

static int probe(struct pci_dev *dev, const struct pci_device_id *id)
{
	return 0;
}

static void remove(struct pci_dev *dev)
{

}
/* used to register the driver with the PCI kernel sub system
 * @see LDD3 page 311
 */
static struct pci_driver pci_driver = {
	.name = DRV_NAME,
	.id_table = ids,
	.probe = probe,
	.remove = remove,
	/* resume, suspend are optional */
};

/**
 * alterapciechdma_init() - Module initialization, registers devices.
 */
static int __init ourpci_init(void)
{
	int rc = 0;
	printk(KERN_DEBUG DRV_NAME " init(), built at " __DATE__ " " __TIME__ "\n");
	/* register this driver with the PCI bus driver */
	rc = pci_register_driver(&pci_driver);
	if (rc < 0)
		return rc;
	return 0;
}
/**
 * alterapciechdma_init() - Module cleanup, unregisters devices.
 */
static void __exit ourpci_exit(void)
{
	printk(KERN_DEBUG DRV_NAME " exit(), built at " __DATE__ " " __TIME__ "\n");
	/* unregister this driver from the PCI bus driver */
	pci_unregister_driver(&pci_driver);
}

MODULE_LICENSE("GPL");

module_init(ourpci_init);
module_exit(ourpci_exit);
