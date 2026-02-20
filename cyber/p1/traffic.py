import os
import csv
from scapy.all import rdpcap, TCP, UDP, ICMP, IP


class Flow:
    def __init__(self, ip_dst, port_dst, ip_src, port_src, protocol):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.port_src = port_src
        self.port_dst = port_dst
        self.protocol = protocol
        self.packets = 0
        self.bytes = 0
        self.closed = False  
        # Start and end times are in Unix timestamp format (seconds since epoch 1970-01-01 00:00:00 UTC)
        self.start_time = None
        self.end_time = None

    def add_packet(self, packet):
        '''
        Add a packet to the flow, updating packet and byte counts, and tracking start/end times.
        '''
        self.packets += 1
        self.bytes += len(packet) 

        # The timestamp updates the flow's start and end times to calculate duration later
        # The value of ts updates for each packet.
        # i.e: packet 1 has ts=0.001, packet 2 has ts=0.002, packet 3 has ts=0.003, etc.
        ts = float(packet.time)  # Packet timestamp
        if self.start_time is None or ts < self.start_time:
            # The start_time corresponds with the first or earliest packet
            self.start_time = ts
        if self.end_time is None or ts > self.end_time:
            # The end_time corresponds with the last or latest packet
            self.end_time = ts

        # Detect TCP flow closure by checking for FIN or RST flags
        if TCP in packet:
            flags = packet[TCP].flags
            # 'F' = FIN, 'R' = RST
            if 'F' in str(flags) or 'R' in str(flags):
                self.closed = True

    def duration(self):
        # In seconds
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        return 0.0

    def avg_packet_size(self):
        return self.bytes / self.packets if self.packets > 0 else 0.0

    def key(self):
        '''
        Returns the 5-tuple that identifies the flow
        '''
        return (self.ip_src, self.ip_dst, self.port_src, self.port_dst, self.protocol)

    def to_dict(self):
        # Used for the later CSV export
        return {
            "start_time": round(self.start_time, 4) if self.start_time is not None else None,
            "end_time": round(self.end_time, 4) if self.end_time is not None else None,
            "ip_dst": self.ip_dst,
            "port_dst": self.port_dst,
            "ip_src": self.ip_src,
            "port_src": self.port_src,
            "protocol": self.protocol,
            "packets": self.packets,
            "bytes": self.bytes,
            "avg_pkt_size": round(self.avg_packet_size(), 2),
            "duration_s": round(self.duration(), 4),
            "closed": self.closed,
        }

# It's the same as the one in tagging.py, but we include it here for modularity
def classify_protocol(packet):
    if ICMP in packet:
        return "ICMP"
    if TCP in packet:
        sport = packet[TCP].sport
        dport = packet[TCP].dport
        if sport == 443 or dport == 443:
            return "HTTPS"
        if sport == 80 or dport == 80:
            return "HTTP"
        return "TCP"
    if UDP in packet:
        sport = packet[UDP].sport
        dport = packet[UDP].dport
        if sport == 53 or dport == 53:
            return "DNS"
        return "UDP"
    return "Otro"


def get_flow_key(packet):
    """
    Obtains the 5-tuple key for a packet to identify its flow.
    Returns None if the packet doesn't have an IP layer.
    The tuple format is: (IP_dst, port_dst, IP_src, port_src, protocol)
    """
    if IP not in packet:
        return None

    ip_src = packet[IP].src
    ip_dst = packet[IP].dst
    # The protocol is determined by the presence of TCP, UDP, or ICMP layers and their ports
    protocol = classify_protocol(packet)

    if TCP in packet:
        port_src = packet[TCP].sport
        port_dst = packet[TCP].dport
    elif UDP in packet:
        port_src = packet[UDP].sport
        port_dst = packet[UDP].dport
    else:
        # ICMP and others do not have ports
        port_src = 0
        port_dst = 0

    return (ip_dst, port_dst, ip_src, port_src, protocol)


def aggregate_flows(pcap_file):
    """
    Reads a pcap file and aggregates packets into flows.
    TCP flows are closed upon detecting FIN/RST and a new one is created
    if the same 5-tuple reappears after closure.
    """
    packets = rdpcap(pcap_file)
    flows = {}  # key -> Flow

    for packet in packets:
        # (ip_src, ip_dst, port_src, port_dst, protocol)
        key = get_flow_key(packet)
        if key is None:
            continue

        # If the flow was already closed, create a new one
        if key in flows and flows[key].closed:
            # Save the closed flow with a unique key (e.g., by appending an index)
            closed_flow = flows.pop(key)
            # Rename the key to store it as closed
            idx = 1
            # *key flattens the tuple key into individual elements for the new key
            while (*key, idx) in flows:
                idx += 1
            flows[(*key, idx)] = closed_flow

        if key not in flows:
            flows[key] = Flow(*key)

        flows[key].add_packet(packet)

    return list(flows.values())


def export_csv(flows, output_path):
    fieldnames = [
        "start_time", "end_time",
        "ip_dst", "port_dst", "ip_src", "port_src",
        "protocol", "packets", "bytes", "avg_pkt_size",
        "duration_s", "closed",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for flow in flows:
            writer.writerow(flow.to_dict())
    print(f"\nCSV exported to: {output_path}")


def print_stats(flows):
    total_packets = sum(f.packets for f in flows)
    total_bytes = sum(f.bytes for f in flows)
    closed_count = sum(1 for f in flows if f.closed)
    open_count = len(flows) - closed_count

    print("=" * 60)
    print("           FLOW STATISTICS")
    print("=" * 60)
    print(f"  Total flows:              {len(flows)}")
    print(f"  Total packets:            {total_packets:,}")
    print(f"  Total bytes:              {total_bytes:,}")
    print(f"  Closed flows (FIN/RST):   {closed_count}")
    print(f"  Open flows:               {open_count}")
    print("=" * 60)

    # Protocol distribution
    protocol_counts = {}
    for f in flows:
        # Key: protocol name, Value: count of flows using that protocol
        protocol_counts[f.protocol] = protocol_counts.get(f.protocol, 0) + 1
    print("\n  Flows by protocol:")
    # Sort protocols by count in descending order and print them
    for proto, count in sorted(protocol_counts.items(), key=lambda x: -x[1]):
        print(f"    {proto:>8}: {count}")

    # Top 3 flows by bytes
    sorted_flows = sorted(flows, key=lambda f: f.bytes, reverse=True)
    print("\n  Top 3 flows by data volume:")
    print(f"  {'#':<4} {'Source IP':<18} {'Destination IP':<18} {'SP':>6} {'DP':>6} {'Proto':<6} {'Pkts':>7} {'Bytes':>12} {'Avg':>10}")
    print("  " + "-" * 92)
    for i, f in enumerate(sorted_flows[:3], 1):
        print(
            f"  {i:<4} {f.ip_src:<18} {f.ip_dst:<18} {f.port_src:>6} {f.port_dst:>6} "
            f"{f.protocol:<6} {f.packets:>7,} {f.bytes:>12,} {f.avg_packet_size():>10,.2f}"
        )
    print()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pcap_file = os.path.join(script_dir, "capture.pcap")
    csv_file = os.path.join(script_dir, "flows.csv")

    print(f"Reading capture: {pcap_file}")
    flows = aggregate_flows(pcap_file)

    print_stats(flows)
    export_csv(flows, csv_file)
