#encoding:utf-8
import os
import sys
import struct
import time
from scapy import all as scapy

class Host(object):
    def __init__(self,name,ifname,mac,ip,port):
        self.hostname=name
        self.ifname=ifname
        self.mac=mac
        self.ip=ip
        self.port=port

class NICTest(object):
    def __init__(self,sender,receiver,inner_sender,inner_receiver):
        self.sender= sender
        self.receiver=receiver
        self.inner_sender=inner_sender
        self.inner_reciver=inner_receiver
    
    def _run_testcase_by_id(self,idx):
        print("<------prepare run testcase%s----->" % idx)
        methods=dir(self)
        #print(methods)
        methods=[m for m in methods if m.startswith('tc%s_'%idx)]
        if len(methods) !=1:
            raise Exception("testcase%s:%s"%(idx,methods))
        print("<------map to function:%s----->" % methods[0])
        fun=getattr(self,methods[0])
        fun()
    def run_testcase(self,name):
        TESTCASE="testcase"
        idx = None
        if not name.startswith(TESTCASE):
            raise Exception("testcase name error")
        try:
            idx=name[len(TESTCASE):]
        except Exception as e:
            raise Exception("testcase number error")
        
        if idx is not None:
            self._run_testcase_by_id(idx)
            return
        raise Exception("UNKNOW")
    
    #构造以太头
    def build_ethhdr(self):
        return scapy.Ether(src=self.sender.mac,dst=self.receiver.mac)
    def build_arp_request(self):
        return scapy.ARP(op=1,psrc=self.sender.ip,hwsrc=self.sender.mac,pdst=self.receiver.ip)
    
    #构造外部ip头
    def build_outer_iphdr(self,is_frag=False,frag_offset=0):
        if is_frag :
            #只支持置为首片或者非首片，不支持置为最后一片
            return scapy.IP(src=self.sender.ip,dst=self.receiver.ip,ttl=10,flags=0x1,frag=frag_offset)
        return scapy.IP(src=self.sender.ip,dst=self.receiver.ip,ttl=10)
    
    #构造icmp头部(echo request)
    def build_icmp_echo_request(self):
        return scapy.ICMP(type=8,code=0)
    
    #构造内部ip头
    def build_inner_iphdr(self,is_frag=False,frag_offset=0):
        if is_frag:
            #只支持置为首片或者非首片，不支持置为最后一片
            return scapy.IP(src=self.inner_sender.ip,dst=self.inner_reciver.ip,ttl=9,flags=0x1,frag=frag_offset)
        return scapy.IP(src=self.inner_sender.ip,dst=self.receiver.ip,ttl=10)
    
    #构造内部udp头
    def build_inner_udphdr(self):
        return scapy.UDP(sport=self.inner_sender.port,dport=self.inner_reciver.port)
    
    #构造外部udp头
    def build_outer_udphdr(self):
        return scapy.UDP(sport=self.sender.port,dport=self.receiver.port)
    
    #构造外部udp头
    def build_outer_tcphdr(self):
        return scapy.TCP(sport=self.sender.port,dport=self.receiver.port,seq=200)
    
    #构造gre头，only_key为True时仅key标记有效
    def build_grehdr(self,only_key=False):
        if only_key:
            return scapy.GRE(key_present=1,key=4096)
        return scapy.GRE(key_present=1,key=4096,chksum_present=1,chksum=0x0a0a,seqnum_present=1,seqence_number=0x0101)
    
    #显示报文内容，用于调试
    def dump_packet(self,p):
        print(p.show())
    
    #向外连续发送报文    
    def send_packet(self,packet):
        #注inter=1表示发送间隔，如果发送间隔过小，遇到目的不可达，kenrel会不回复icmp报文
        scapy.sendp(packet,iface=self.sender.ifname,loop=1,verbose=0,inter=2)
        
    #
    # 用例：非gre报文分流到kernel(arp报文）
    def tc1_ethhdr__arphdr_rquest(self):
        #正常的以太头，arp请求头
        ethhdr=self.build_ethhdr()
        arphdr_request=self.build_arp_request()
        packet=ethhdr/arphdr_request
        self.dump_packet(packet)
        self.send_packet(packet)  
        
    #
    # 用例：非gre报文分流到kernel(icmp报文,echo request）
    def tc2_ethhdr__icmphdr_echo_request(self):
        #正常的以太头，正常的ip头，icmp报文
        ethhdr=self.build_ethhdr()
        iphdr=self.build_outer_iphdr()
        icmp_echo=self.build_icmp_echo_request()
        payload="<playload>"
        packet=ethhdr/iphdr/icmp_echo/payload
        self.dump_packet(packet)
        self.send_packet(packet)
    
    #
    # 用例：非gre报文分流到kernel(tcp报文）
    def tc3_ethhdr__tcphdr(self):
        #正常的以太头，正常的ip头，未监听的tcp port
        #存在主机回复icmp(3,10)报文，目的不可达
        ethhdr=self.build_ethhdr()
        iphdr=self.build_outer_iphdr()
        tcphdr=self.build_outer_tcphdr()
        payload="<playload>"
        packet=ethhdr/iphdr/tcphdr/payload
        self.dump_packet(packet)
        self.send_packet(packet)
            
    #
    # 用例：非gre报文分流到kernel（udp报文）
    def tc4_ethhdr__udphdr(self):
        #正常的以太头，正常的ip头，未监听的udp port
        #主机回复目的不可达
        ethhdr=self.build_ethhdr()
        iphdr=self.build_outer_iphdr()
        udphdr=self.build_outer_udphdr()
        payload="<playload>"
        packet=ethhdr/iphdr/udphdr/payload
        self.dump_packet(packet)
        self.send_packet(packet)
    
    #
    #用例：gre报文分流dpdk(内部udp报文）
    def tc5_ethhdr__outeriphdr__gre__inneriphdr__udp(self):
        #正常的以太头，外层ip头（非分片），gre头（含key,checksum,seq),内层ip头（非分片），udp头（完整）
        ethhdr=self.build_ethhdr()
        outer_iphdr = self.build_outer_iphdr()
        grehdr = self.build_grehdr(only_key=False)
        inner_iphdr = self.build_inner_iphdr()
        inner_udphdr=self.build_inner_udphdr()
        udp_payload="<payload>"
        packet= ethhdr/outer_iphdr/grehdr/inner_iphdr/inner_udphdr/udp_payload
        self.dump_packet(packet)
        self.send_packet(packet)
    
    #
    #用例：外层ipv4分片（GRE无负载）对投递无影响
    def tc6_ethhdr__outeriphdr_f_gre__(self):
        #正常的以太头，外层ip头（首片），gre头（仅包含key)
        ethhdr=self.build_ethhdr()
        outeriphdr_f = self.build_outer_iphdr(is_frag=True,frag_offset=0)
        grehdr=self.build_grehdr(only_key=True)
        #innerhdr=self.build_inner_iphdr()
        packet=ethhdr/outeriphdr_f/grehdr
        self.dump_packet(packet)
        self.send_packet(packet)
        
    #
    #用例：特征不同的gre内层报文（非分片）可投递到不同队列
    def tc7_ethhdr__gre__inneriphdr__tcp_udp(self,skip_send=0,only_key=True,is_frag=False,frag_offset=0,inner_ip_protocol=0):
        def __build_incomplete_tcp_packet(obj,srcport=0,dstport=0):
            return struct.pack('!H',srcport)
        def __build_tcp_packet(obj,srcport=0,dstport=0):
            return scapy.TCP(sport=srcport,dport=dstport)
        
        def __build_udp_packet(obj,srcport=0,dstport=0):
            return scapy.UDP(sport=srcport,dport=dstport)
            
        def __build_packet(obj,payload):
            ethhdr=obj.build_ethhdr()
            outer_iphdr = obj.build_outer_iphdr()
            grehdr = obj.build_grehdr(only_key=only_key)
            inner_iphdr = self.build_inner_iphdr(is_frag=is_frag,frag_offset=frag_offset)
            if inner_ip_protocol:
                inner_iphdr.proto=inner_ip_protocol
            packet=ethhdr/outer_iphdr/grehdr/inner_iphdr/payload
            return packet
        
        packet_tcp = __build_packet(self,__build_tcp_packet(self,srcport=33428,dstport=34619))
        packet_udp = __build_packet(self,__build_udp_packet(self,srcport=34619,dstport=33428))
        packet_incomplete_tcp = __build_packet(self,__build_incomplete_tcp_packet(self,srcport=33428,dstport=34619))
        #self.dump_packet(packet_incomplete_tcp)
        if skip_send:
            return packet_tcp,packet_udp,packet_incomplete_tcp
        
        self.dump_packet(packet_tcp)
        self.dump_packet(packet_udp)
        while True:
            scapy.sendp(packet_tcp,iface=self.sender.ifname,loop=0,verbose=0)
            scapy.sendp(packet_udp,iface=self.sender.ifname,loop=0,verbose=0)
            time.sleep(2)
    
    #
    #用例：Gre头部长度增加对投递无影响
    def tc8_ethhdr__gre_l_inneriphdr__tcp_udp(self):
            self.tc_ethhdr__gre__inneriphdr__tcp_udp(skip_send=0,only_key=False)
            
    #
    # 用例：内层分片（ipv4首片，完整l4头）对投递无影响
    def tc9_ethhdr__gre__inneriphdr_f_tcp(self):
        #正常的以太头，外层ip头（非分片），gre头,内层ip头（首个分片），tcp头（完整）
        packet_tcp,_,_=self.tc_ethhdr__gre__inneriphdr__tcp_udp(skip_send=1,only_key=True,is_frag=True,frag_offset=0)
        self.dump_packet(packet_tcp)
        self.send_packet(packet_tcp)
        
    #
    # 用例：内层分片（ipv4首片，非完整l4头）对投递无影响
    def tc10_ethhdr__gre__inneriphdr_f_tcp_i_(self):
        #正常的以太头，外层ip头（非分片），gre头,内层ip头（首个分片），tcp头（不完整,仅包含tcp头部的srcport）
        _,_,packet_incomplete_tcp=self.tc_ethhdr__gre__inneriphdr__tcp_udp(skip_send=1,only_key=True,is_frag=True,frag_offset=0,inner_ip_protocol=6)
        self.dump_packet(packet_incomplete_tcp)
        self.send_packet(packet_incomplete_tcp)
    
    #
    # 用例：内层分片（ipv4非首片）对投递无影响
    def tc11_ethhdr__gre__inneriphdr_mf_tcp(self):
        #正常的以太头，外层ip头（非分片），gre头,内层ip头（非首个分片），tcp头（完整）
        packet_tcp,_,_=self.tc_ethhdr__gre__inneriphdr__tcp_udp(skip_send=1,only_key=True,is_frag=True,frag_offset=100)
        self.dump_packet(packet_tcp)
        self.send_packet(packet_tcp)
        
    #
    # 用例：网卡收到gre内层错误的ipv4 checksum
    def tc12_ethhdr__gre__inneriphdr_ec_udp(self):
        #正常的以太头，外层ip头（非分片），gre头（含key,checksum,seq),内层ip头（非分片,checksum错误），udp头（完整）
        ethhdr=self.build_ethhdr()
        outer_iphdr = self.build_outer_iphdr()
        grehdr = self.build_grehdr(only_key=False)
        inner_iphdr = self.build_inner_iphdr()
        #error checksum
        inner_iphdr.chksum = 0x99
        inner_udphdr=self.build_inner_udphdr()
        udp_payload="<payload>"
        packet= ethhdr/outer_iphdr/grehdr/inner_iphdr/inner_udphdr/udp_payload
        self.dump_packet(packet)
        self.send_packet(packet)
    
    #
    # 用例：网卡gre内层ipv4 checksum offload
    def tc13_ethhdr__gre__inneriphdr_nc_tcp(self):
        pass
    
    #
    # 用例：内层rss分流均匀测试
    def tc14_ethhdr__gre__inneriphdr__udp(self):
        #正常的以太头，外层ip头（非分片），gre头（含key,checksum,seq),内层ip头（非分片），udp头（完整）
        ethhdr=self.build_ethhdr()
        outer_iphdr = self.build_outer_iphdr()
        grehdr = self.build_grehdr(only_key=False)
        inner_iphdr = self.build_inner_iphdr()
        inner_udphdr=self.build_inner_udphdr()
        udp_payload="<payload>"
        for i in range(2000,62000):
            inner_udphdr.sport = i
            inner_udphdr.dport = i
            packet= ethhdr/outer_iphdr/grehdr/inner_iphdr/inner_udphdr/udp_payload
            #self.dump_packet(packet)
            scapy.sendp(packet,iface=self.sender.ifname,loop=0,verbose=0)
            #if i %32:
            #    time.sleep(0.01)
    
def main():
    sender = Host('sender','enp0s31f6','30:9c:23:73:aa:08','10.10.10.11',5555)
    receiver = Host('receiver','eth1','08:00:27:d6:07:21','10.10.10.8',4444)
    inner_sender   = Host('inner_sender','eth0','00:00:11:11:11:11','2.2.2.2',17345)
    inner_receiver = Host('inner_receiver','eth0','00:00:00:01:02:03','3.3.3.3',27345)
    test=NICTest(sender,receiver,inner_sender,inner_receiver)
    test.run_testcase(os.path.basename(sys.argv[0]))
    
if __name__ == "__main__":
    sender = Host('sender','enp0s31f6','30:9c:23:73:aa:08','10.10.10.11',5555)
    receiver = Host('receiver','eth1','08:00:27:d6:07:21','10.10.10.8',4444)
    inner_sender   = Host('inner_sender','eth0','00:00:11:11:11:11','2.2.2.2',17345)
    inner_receiver = Host('inner_receiver','eth0','00:00:00:01:02:03','3.3.3.3',27345)
    test=NICTest(sender,receiver,inner_sender,inner_receiver)
    #test.tc_ethhdr__outeriphdr_f_gre__()
    #test.tc_ethhdr__outeriphdr__gre__inneriphdr__udp()
    #test.tc_ethhdr__arphdr_rquest()
    #test.tc_ethhdr__icmphdr_echo_request()
    #test.tc_ethhdr__udphdr()
    #test.tc_ethhdr__tcphdr()
    #test.tc_ethhdr__gre__inneriphdr__tcp_udp()
    #test.tc_ethhdr__gre_l_inneriphdr__tcp_udp()
    #test.tc_ethhdr__gre__inneriphdr_f_tcp()
    #test.tc_ethhdr__gre__inneriphdr_f_tcp_i_()
    #test.tc_ethhdr__gre__inneriphdr_mf_tcp()
    #test.tc_ethhdr__gre__inneriphdr_ec_udp()
    #test.run_testcase("testcase1")
    test.tc14_ethhdr__gre__inneriphdr__udp()
    