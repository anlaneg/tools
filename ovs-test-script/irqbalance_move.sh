#! /bin/bash

#IRQ 有一个关联的“类似”属性 smp_affinity，该参数可以定义允许为 IRQ 执行 ISR 的 CPU 核。
#这个属性还用来提高程序性能，方法是为一个或者多个具体 CPU 核分配中断类似性和程序线程类似性。
#这可让缓存线可在指定的中断和程序线程之间共享。
#具体 IRQ 数的中断近似性值是保存的相关的 /proc/irq/IRQ_NUMBER/smp_affinity 文件中，
#您可以作为 root 用户查看并修改该值。保存在这个文件中的值是一个十六进制字节掩码，代表系统中所有 CPU 核。

#smp_affinity 的默认值为 f，即可为系统中任意 CPU 提供 IRQ。将这个值设定为 1，如下，即表示只有 CPU 0 可以提供这个中断：
# echo 1 >/proc/irq/32/smp_affinity
# cat /proc/irq/32/smp_affinity
#1

#move IRQ 
smp_affinity_mask=1

irqs=`ls /proc/irq` 

function set_irq_smp_affinity()
{
	success_irqs=""
	fail_irqs=""

	for i in ${irqs} ; 
	do 
		if [ -f /proc/irq/$i/smp_affinity ]; 
		then 
			#echo "echo $smp_affinity_mask > /proc/irq/$i/smp_affinity" 
			echo $smp_affinity_mask > /proc/irq/$i/smp_affinity  2>/dev/null
			mask=`cat /proc/irq/$i/smp_affinity`
			if [ $((16#$mask)) -ne $((16#$smp_affinity_mask)) ];
			then
				fail_irqs="$fail_irqs $i"
			else
				success_irqs="$success_irqs $i"
			fi;
		fi 
	done 
	echo "modify irq $success_irqs  successfully"
	echo "modify irq $fail_irqs fail"
}

function stop_and_disable_service()
{
	services="irqbalance firewalld auditd kdump NetworkManager"
	for i in ${services};
	do
		systemctl stop $i.service
		systemctl disable $i.service
		
	done;
}

user_id=`id -u`
if [ $user_id -ne 0 ];
then
	echo "Permission denied"
	exit
else
	killall irqbalance 
	set_irq_smp_affinity
	stop_and_disable_service
fi;
