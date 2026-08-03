"""Generate deterministic industrial-security traffic for Suricata testing.

The generated PCAP contains three TCP payload packets:

1. Unauthorized OPC-UA access marker on TCP/4840
2. Suspicious MQTT command marker on TCP/1883
3. Suspicious FUXA HMI access marker on TCP/1881

Only the Python standard library is used.
"""

from __future__ import annotations

import ipaddress
import struct
import time
from pathlib import Path


OUTPUT_PATH = Path(
    "suricata/pcaps/topic127_industrial_ids_test.pcap"
)

SOURCE_MAC = bytes.fromhex("020000000001")
DESTINATION_MAC = bytes.fromhex("020000000002")

SOURCE_IP = "192.0.2.50"
DESTINATION_IP = "192.0.2.100"

PACKETS = [
    {
        "source_port": 41001,
        "destination_port": 4840,
        "payload": b"TOPIC127-UNAUTHORIZED-OPCUA",
    },
    {
        "source_port": 41002,
        "destination_port": 1883,
        "payload": b"TOPIC127-MQTT-TAMPER",
    },
    {
        "source_port": 41003,
        "destination_port": 1881,
        "payload": b"TOPIC127-HMI-SCAN",
    },
]


def internet_checksum(data: bytes) -> int:
    """Return the RFC 1071 Internet checksum."""

    if len(data) % 2:
        data += b"\x00"

    total = sum(
        struct.unpack(
            f"!{len(data) // 2}H",
            data,
        )
    )

    while total >> 16:
        total = (
            total & 0xFFFF
        ) + (
            total >> 16
        )

    return (~total) & 0xFFFF


def build_ipv4_tcp_packet(
    *,
    source_port: int,
    destination_port: int,
    payload: bytes,
    sequence_number: int,
) -> bytes:
    """Build one Ethernet/IPv4/TCP packet."""

    source_ip = ipaddress.IPv4Address(
        SOURCE_IP
    ).packed

    destination_ip = ipaddress.IPv4Address(
        DESTINATION_IP
    ).packed

    # Ethernet II header: destination, source, IPv4 EtherType.
    ethernet_header = (
        DESTINATION_MAC
        + SOURCE_MAC
        + struct.pack("!H", 0x0800)
    )

    tcp_header_length = 20
    ip_header_length = 20
    total_length = (
        ip_header_length
        + tcp_header_length
        + len(payload)
    )

    version_and_ihl = 0x45
    type_of_service = 0
    identification = sequence_number & 0xFFFF
    flags_and_fragment_offset = 0x4000
    time_to_live = 64
    protocol = 6

    ip_header_without_checksum = struct.pack(
        "!BBHHHBBH4s4s",
        version_and_ihl,
        type_of_service,
        total_length,
        identification,
        flags_and_fragment_offset,
        time_to_live,
        protocol,
        0,
        source_ip,
        destination_ip,
    )

    ip_checksum = internet_checksum(
        ip_header_without_checksum
    )

    ip_header = struct.pack(
        "!BBHHHBBH4s4s",
        version_and_ihl,
        type_of_service,
        total_length,
        identification,
        flags_and_fragment_offset,
        time_to_live,
        protocol,
        ip_checksum,
        source_ip,
        destination_ip,
    )

    data_offset = 5
    flags = 0x18  # PSH + ACK
    offset_and_flags = (
        data_offset << 12
    ) | flags

    tcp_header_without_checksum = struct.pack(
        "!HHIIHHHH",
        source_port,
        destination_port,
        sequence_number,
        1,
        offset_and_flags,
        64240,
        0,
        0,
    )

    pseudo_header = struct.pack(
        "!4s4sBBH",
        source_ip,
        destination_ip,
        0,
        protocol,
        tcp_header_length + len(payload),
    )

    tcp_checksum = internet_checksum(
        pseudo_header
        + tcp_header_without_checksum
        + payload
    )

    tcp_header = struct.pack(
        "!HHIIHHHH",
        source_port,
        destination_port,
        sequence_number,
        1,
        offset_and_flags,
        64240,
        tcp_checksum,
        0,
    )

    return (
        ethernet_header
        + ip_header
        + tcp_header
        + payload
    )


def write_pcap(
    path: Path,
    packets: list[bytes],
) -> None:
    """Write packets using the classic PCAP format."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Little-endian PCAP global header.
    global_header = struct.pack(
        "<IHHIIII",
        0xA1B2C3D4,
        2,
        4,
        0,
        0,
        65535,
        1,  # Ethernet
    )

    timestamp = int(time.time())

    with path.open("wb") as handle:
        handle.write(global_header)

        for index, packet in enumerate(
            packets,
            start=1,
        ):
            packet_header = struct.pack(
                "<IIII",
                timestamp + index,
                0,
                len(packet),
                len(packet),
            )

            handle.write(packet_header)
            handle.write(packet)


def main() -> None:
    generated_packets = []

    for index, definition in enumerate(
        PACKETS,
        start=1,
    ):
        generated_packets.append(
            build_ipv4_tcp_packet(
                source_port=definition[
                    "source_port"
                ],
                destination_port=definition[
                    "destination_port"
                ],
                payload=definition["payload"],
                sequence_number=1000 * index,
            )
        )

    write_pcap(
        OUTPUT_PATH,
        generated_packets,
    )

    print(
        "Generated packets :",
        len(generated_packets),
    )
    print(
        "Source IP         :",
        SOURCE_IP,
    )
    print(
        "Destination IP    :",
        DESTINATION_IP,
    )

    for definition in PACKETS:
        print(
            "Detection traffic:",
            f"TCP/{definition['destination_port']}",
            definition["payload"].decode(
                "ascii"
            ),
        )

    print(
        "Written           :",
        OUTPUT_PATH,
    )
    print(
        "PCAP size         :",
        OUTPUT_PATH.stat().st_size,
        "bytes",
    )
    print(
        "Suricata deterministic test PCAP generation: PASS"
    )


if __name__ == "__main__":
    main()
