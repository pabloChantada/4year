import os
from scapy.all import rdpcap, TCP, UDP, ICMP, DNS, IP

def label_packets(pcap_file):
    packets = rdpcap(pcap_file)
    labeled_packets = []

    for packet in packets:
        label = 'Otro'
        
        # Check for ICMP
        if ICMP in packet:
            label = 'ICMP'

        # Check for TCP (HTTP or HTTPS)
        elif TCP in packet:
            tcp_layer = packet[TCP]
            dest_port = tcp_layer.dport
            src_port = tcp_layer.sport
            
            # Reserved ports for HTTP are 80 and for HTTPS are 443
            if dest_port == 443 or src_port == 443:
                label = 'HTTPS'
            elif dest_port == 80 or src_port == 80:
                label = 'HTTP'

        # Check for UDP (DNS)
        elif UDP in packet:
            udp_layer = packet[UDP]
            dest_port = udp_layer.dport
            src_port = udp_layer.sport
            
            # Reserved ports for DNS are 53
            if dest_port == 53 or src_port == 53:
                label = 'DNS'
        
        # Add the packet and its label to the list
        labeled_packets.append((packet, label))
    
    return labeled_packets

def print_labeled_packets(labeled_packets):
    type_counts = {
        'HTTP': 0,
        'HTTPS': 0,
        'DNS': 0,
        'ICMP': 0,
        'Otro': 0
    }
    
    for packet, label in labeled_packets:
        print(f"Packet: {packet.summary()} - Label: {label}")
        type_counts[label] += 1

    # Print the counts of each packet type 
    print("\nPacket Type Counts:")
    for label, count in type_counts.items():
        print(f"{label}: {count}")

if __name__ == "__main__":
    # Obtain the pcap file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pcap_file = os.path.join(script_dir, "capture.pcap")
    labeled_packets = label_packets(pcap_file)
    
    print_labeled_packets(labeled_packets)


'''
Packet Type Counts:
HTTP: 30
HTTPS: 6453
DNS: 52
ICMP: 0
Otro: 44

--- 

Output actual -> en la captura no hay ICMP:
'''