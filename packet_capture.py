import scapy.all as scapy
import netifaces as ni
import winreg as wr
import time
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler

encoder = OneHotEncoder(handle_unknown='ignore')
scaler = StandardScaler()

isolation_forest_model = joblib.load('isolation_forest_model.pkl')
isolation_forest_encoder = joblib.load('isolation_forest_encoder.pkl')
isolation_forest_scaler = joblib.load('isolation_forest_scaler.pkl')

one_class_svm_model = joblib.load('one_class_svm_model.pkl')
one_class_svm_encoder = joblib.load('one_class_svm_encoder.pkl')
one_class_svm_scaler = joblib.load('one_class_svm_scaler.pkl')

average_bandwidth = joblib.load('average_bandwidth.pkl') 

overall_average_bandwidth = sum(average_bandwidth.values()) / 24 
overall_bandwidth_threshold = overall_average_bandwidth * 2

known_ips = set() 

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

def sniff_wifi(interface, output_file):
    try:
        scapy.sniff(iface=interface, filter="tcp or udp", prn=lambda packet: process_packet(packet, output_file))
        time.sleep(0.01)
    except:
        pass

def process_packet(packet, output_file):
    try:
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst

        if packet.haslayer(scapy.TCP):
            src_port = packet[scapy.TCP].sport
            dst_port = packet[scapy.TCP].dport
            protocol = "TCP"
            tcp_flags = packet[scapy.TCP].flags
            info = packet.summary() + f" [TCP Flags: {tcp_flags}]" 
        else: 
            src_port = packet[scapy.UDP].sport
            dst_port = packet[scapy.UDP].dport
            protocol = "UDP"
            info = packet.summary() + " [UDP]"

        length = len(packet)
        size = len(packet) * 8

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        packet_data = pd.DataFrame([[src_ip, dst_ip, src_port, dst_port, protocol, length, timestamp]],
                                   columns=['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'length', 'timestamp'])
        
        packet_data = preprocess_data(packet_data, one_class_svm_encoder, one_class_svm_scaler)

        isolation_forest_prediction = isolation_forest_model.predict(packet_data)
        one_class_svm_prediction = one_class_svm_model.predict(packet_data)

        category, anomaly_type, threat_level = categorize_anomaly(isolation_forest_prediction, one_class_svm_prediction, packet, average_bandwidth)

        if isolation_forest_prediction == -1 or one_class_svm_prediction == -1:
            with open(output_file, 'a') as f:
                f.write(f"{timestamp} | {' | '.join(map(str, [src_ip, src_port, dst_ip, dst_port, length, size, info, category, threat_level]))}\n")

    except:
        pass

def preprocess_data(data, encoder, scaler):
    categorical_cols = ['protocol']
    encoded_cols = pd.DataFrame(encoder.transform(data[categorical_cols]).toarray())
    data = data.drop(categorical_cols, axis=1)
    data = pd.concat([data, encoded_cols], axis=1)

    numerical_cols = ['src_port', 'dst_port', 'length']
    data[numerical_cols] = scaler.transform(data[numerical_cols])

    return data

def categorize_anomaly(isolation_forest_prediction, one_class_svm_prediction, packet, average_bandwidth):
    if isolation_forest_prediction == -1 or one_class_svm_prediction == -1:
        is_anomaly = True
    else:
        is_anomaly = False

    if not is_anomaly:
        return "Normal", "None", "None"

    if packet[scapy.IP].src not in known_ips:
        known_ips.add(packet[scapy.IP].src)
        return "IP", "New IP", "Minimal"

    elif packet[scapy.IP].src.startswith('10.') : 
        return "IP", "Unusual/Suspicious IP", "Average"

    current_hour = time.localtime().tm_hour
    hourly_bandwidth_threshold = average_bandwidth.get(current_hour, 0) * 1.5

    if packet.length > hourly_bandwidth_threshold:
        return "Bandwidth", "High bandwidth usage on a time that should not happen", "Average"
    elif packet.length > overall_bandwidth_threshold:
        return "Bandwidth", "Very high bandwidth usage", "Critical"

    return "Suspicious Activity", "Suspicious/unusual network activity", "Critical"

if __name__ == "__main__":
    interface = get_active_interface()
    output_file = 'anomaly_log.txt' 

    if interface:
        print(f"Sniffing on interface: {interface}")
        sniff_wifi(interface, output_file)
    else:
        print("Error: No active network interface found.") 