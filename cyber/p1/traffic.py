import os
import csv
from scapy.all import rdpcap, TCP, UDP, ICMP, IP
from collections import defaultdict
from datetime import datetime


class Flow:
    """Clase para representar un flujo de tráfico"""
    
    def __init__(self, flow_id, src_ip, src_port, dst_ip, dst_port, protocol, timestamp):
        self.flow_id = flow_id
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.protocol = protocol
        self.start_time = timestamp
        self.end_time = timestamp
        
        # Características del flujo
        self.packet_count = 0
        self.total_bytes = 0
        self.tcp_flags = set()
        self.is_closed = False
        self.payload_bytes = 0
        self.min_ttl = float('inf')
        self.max_ttl = 0
        
    def add_packet(self, packet, packet_size):
        """Añade un paquete al flujo"""
        self.packet_count += 1
        self.total_bytes += packet_size
        self.end_time = packet.time if hasattr(packet, 'time') else self.end_time
        
        # Extraer TTL si está disponible
        if IP in packet:
            ip_layer = packet[IP]
            ttl = ip_layer.ttl
            self.min_ttl = min(self.min_ttl, ttl)
            self.max_ttl = max(self.max_ttl, ttl)
            
            # Calcular payload (datos de aplicación)
            payload_size = len(packet) - len(ip_layer)
            self.payload_bytes += max(0, payload_size)
        
        # Extraer flags TCP si está disponible
        if TCP in packet:
            tcp_layer = packet[TCP]
            flags = tcp_layer.flags
            self.tcp_flags.add(flags)
            
            # Verificar si el flujo debe cerrarse (FIN o RST)
            if flags & 0x01 or flags & 0x04:  # FIN = 0x01, RST = 0x04
                self.is_closed = True
    
    def get_duration(self):
        """Calcula la duración del flujo en segundos"""
        if isinstance(self.start_time, float) and isinstance(self.end_time, float):
            return self.end_time - self.start_time
        return 0
    
    def to_dict(self):
        """Convierte el flujo a un diccionario"""
        return {
            'flow_id': self.flow_id,
            'src_ip': self.src_ip,
            'src_port': self.src_port,
            'dst_ip': self.dst_ip,
            'dst_port': self.dst_port,
            'protocol': self.protocol,
            'start_time': datetime.fromtimestamp(self.start_time).isoformat() if isinstance(self.start_time, float) else str(self.start_time),
            'duration_seconds': round(self.get_duration(), 4),
            'packet_count': self.packet_count,
            'total_bytes': self.total_bytes,
            'payload_bytes': self.payload_bytes,
            'avg_packet_size': round(self.total_bytes / self.packet_count, 2) if self.packet_count > 0 else 0,
            'min_ttl': self.min_ttl if self.min_ttl != float('inf') else 'N/A',
            'max_ttl': self.max_ttl,
            'tcp_flags': str(self.tcp_flags) if self.tcp_flags else 'N/A',
            'is_closed': self.is_closed
        }


def get_flow_id(packet):
    """
    Genera un identificador único para un flujo basado en:
    (IP origen, puerto origen, IP destino, puerto destino, protocolo)
    """
    if IP not in packet:
        return None
    
    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    protocol = ip_layer.proto
    
    # Determinar puertos según el protocolo
    src_port = None
    dst_port = None
    
    if TCP in packet:
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        protocol_name = 'TCP'
    elif UDP in packet:
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        protocol_name = 'UDP'
    elif ICMP in packet:
        src_port = 0
        dst_port = 0
        protocol_name = 'ICMP'
    else:
        src_port = 0
        dst_port = 0
        protocol_name = f'Other({protocol})'
    
    # Crear ID: (src_ip, src_port, dst_ip, dst_port, protocolo)
    flow_id = f"{src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol_name}]"
    
    return flow_id, src_ip, src_port, dst_ip, dst_port, protocol_name


def extract_flows(pcap_file):
    """
    Extrae los flujos de tráfico del archivo .pcap
    """
    try:
        packets = rdpcap(pcap_file)
        print(f"Se cargaron {len(packets)} paquetes\n")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return []
    
    active_flows = {}  # Diccionario de flujos activos
    closed_flows = []  # Lista de flujos cerrados
    
    for packet in packets:
        flow_info = get_flow_id(packet)
        
        if flow_info is None:
            continue
        
        flow_id, src_ip, src_port, dst_ip, dst_port, protocol = flow_info
        packet_size = len(packet)
        
        # Verificar si el flujo ya existe
        if flow_id not in active_flows:
            # Crear nuevo flujo
            flow = Flow(flow_id, src_ip, src_port, dst_ip, dst_port, protocol, packet.time)
            active_flows[flow_id] = flow
        
        # Añadir el paquete al flujo
        flow = active_flows[flow_id]
        flow.add_packet(packet, packet_size)
        
        # Verificar si el flujo debe cerrarse
        if flow.is_closed:
            closed_flows.append(active_flows.pop(flow_id))
    
    # Los flujos que siguen activos al final de la captura también se cierran
    closed_flows.extend(active_flows.values())
    
    print(f"Se extrajeron {len(closed_flows)} flujos de tráfico\n")
    
    return closed_flows


def save_flows_to_csv(flows, output_file):
    """
    Guarda los flujos en un archivo CSV
    """
    if not flows:
        print("No hay flujos para guardar")
        return
    
    try:
        # Obtener las claves del primer flujo
        fieldnames = list(flows[0].to_dict().keys())
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for flow in flows:
                writer.writerow(flow.to_dict())
        
        print(f"Flujos guardados en: {output_file}")
        
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")


def main():
    # Obtener la ruta del directorio donde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pcap_file = os.path.join(script_dir, "capture.pcap")
    output_file = os.path.join(script_dir, "flows.csv")
    
    # Extraer flujos
    flows = extract_flows(pcap_file)
    
    # Mostrar estadísticas
    print(f"{'='*70}")
    print("ESTADÍSTICAS DE FLUJOS")
    print(f"{'='*70}")
    print(f"Total de flujos: {len(flows)}")
    
    # Contar flujos por protocolo
    protocol_counts = defaultdict(int)
    for flow in flows:
        protocol_counts[flow.protocol] += 1
    
    print("\nFlujos por protocolo:")
    for protocol, count in protocol_counts.items():
        print(f"  {protocol}: {count}")
    
    # Guardar flujos en CSV
    save_flows_to_csv(flows, output_file)


if __name__ == "__main__":
    main()