#!/usr/bin/make -f

#压缩包的名字必须是包含文件名及版本号
package?=hello-17.7.6.tar.gz
temp-dir:=$(CURDIR)/tmp

build-deb:build-tmp-dir package-extra
	( cd `find $(temp-dir) -depth -maxdepth 1 -type d | head -n 1` ; \
	  dh_make -s -y -f ../$(package)  ; \
	  dpkg-buildpackage ;\
	  mv ../*.deb $(CURDIR); \
	)
	rm -rf $(temp-dir)

clean:
	rm -rf $(temp-dir)
	rm -rf *.deb	

build-tmp-dir:
	mkdir -p $(temp-dir)

extra-%.tar.gz:$(package)
	cp $< $(temp-dir)
	tar -zxvf $(package) -C $(temp-dir)

extra-%.tar:$(package)
	cp $< $(temp-dir)
	tar -xvf $(package) -C $(temp-dir)

package-extra:extra-$(package)
