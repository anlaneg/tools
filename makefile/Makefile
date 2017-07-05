
define my_func
@echo "hello my func $(1)"
endef

all:/an.c
	echo $(CURDIR)
	echo $(OS_ID)
	echo $(MAKEFILE_LIST)
	echo "--$(an)--"
ifeq (1,1)
	echo "1"
else
	echo "0"
endif
#Makefile comment
	#shell comment
	$(my_func)
	$(call my_func ,argment)






#此目标将被合并
/an.c:test
/an.c:export an='anf' 
/an.c:bn
	echo "an.c"
	echo "$(an)"

test:
	@echo "----help"
bn:
	@echo "---bn"

#test1:/home/anlang/workspace/anlaneg_tools/makefile/yumdownloader
#/home/anlang/workspace/anlaneg_tools/makefile/yumdownloader:

define build
@echo "###$1---$2###"
endef


test1:
	echo "hello"
	$(call build,'anf')


