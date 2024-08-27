import scapy.all as scapy
import netifaces as ni
import winreg as wr
import time
import pandas as pd
import os


def get_connection_name_from_guid(iface_guids):
    iface_names = ['(unknown)' for i in range(len(iface_guids))]
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in range(len(iface_guids)):
        try:
            reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
            iface_names[i] = wr.QueryValueEx(reg_subkey, 'Name')[0]
        except FileNotFoundError:
            pass
    return iface_names

def get_active_interface(preferred_type='Ethernet'):
    iface_guids = ni.interfaces()
    iface_names = get_connection_name_from_guid(iface_guids)

    for i, iface_guid in enumerate(iface_guids):
        addrs = ni.ifaddresses(iface_guid)
        if ni.AF_INET in addrs and addrs[ni.AF_INET][0]['addr'] != '127.0.0.1':
            if preferred_type in iface_names[i]:
                return iface_names[i]

    for i, iface_guid in enumerate(iface_guids):
        addrs = ni.ifaddresses(iface_guid)
        if ni.AF_INET in addrs and addrs[ni.AF_INET][0]['addr'] != '127.0.0.1':
            return iface_names[i]
    return None

def sniff_wifi(interface):
    try:
        scapy.sniff(iface=interface, filter="tcp or udp", prn=lambda packet: process_packet(packet))
        time.sleep(0.01)
    except:
        pass

def process_packet(packet):
    try:
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst

        if packet.haslayer(scapy.TCP):
            src_port = packet[scapy.TCP].sport
            dst_port = packet[scapy.TCP].dport
            protocol = "TCP"
        else:
            src_port = packet[scapy.UDP].sport
            dst_port = packet[scapy.UDP].dport
            protocol = "UDP"

        length = len(packet)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        packet_data = pd.DataFrame([[src_ip, dst_ip, src_port, dst_port, protocol, length, timestamp]],
                                   columns=['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'length', 'timestamp'])

        current_date = time.strftime("%Y-%m-%d")
        output_file = f'captured_packets_{current_date}.csv'
        packet_data.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

    except:
        pass

if __name__ == "__main__":
    interface = get_active_interface()

    if interface:
        print(f"Sniffing on interface: {interface}")

        end_time = time.time() + 60 * 60 * 24 * 14

        while time.time() < end_time:
            sniff_wifi(interface)

    else:
        print("Error: No active network interface found.")
