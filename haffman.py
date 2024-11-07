import heapq
import os
from collections import Counter, namedtuple

def build_frequency_table(data):
    return Counter(data)


def build_huffman_tree(frequency_table):
    heap = [HuffmanNode(freq, symbol, None, None) for symbol, freq in frequency_table.items()]
    heapq.heapify(heap)
    if len (heap) == 1:
        return HuffmanNode(heap[0].frequency, None, heap[0],None )
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged_node = HuffmanNode(left.frequency + right.frequency, None, left, right)
        heapq.heappush(heap, merged_node)
    return heap[0] if heap else None


def build_huffman_codes(node, prefix="", code_table={}):
    if node is not None:
        if node.symbol is not None:
            code_table[node.symbol] = prefix
        build_huffman_codes(node.left, prefix + "0", code_table)
        build_huffman_codes(node.right, prefix + "1", code_table)
    return code_table


def compress_data(data, code_table):
    return "".join(code_table[byte] for byte in data)


def save_compressed_file(output_path, compressed_data, code_table, file_extension):
    with open(output_path, "wb") as f:
        # Save file extension length and extension itself
        f.write(len(file_extension).to_bytes(1, 'big'))
        f.write(file_extension.encode())

        # Save the frequency table
        f.write(len(code_table).to_bytes(4, 'big'))
        for symbol, code in code_table.items():
            f.write(symbol.to_bytes(1, 'big'))
            f.write(len(code).to_bytes(1, 'big'))
            f.write(int(code, 2).to_bytes((len(code) + 7) // 8, 'big'))

        # Calculate padding required to make binary data a multiple of 8
        padding_length = (8 - len(compressed_data) % 8) % 8
        compressed_data += '0' * padding_length

        # Store padding information and write compressed data
        f.write(padding_length.to_bytes(1, 'big'))
        binary_data = int(compressed_data, 2).to_bytes(len(compressed_data) // 8, 'big')
        f.write(len(compressed_data).to_bytes(4, 'big'))
        f.write(binary_data)

class HuffmanNode(namedtuple("Node", ["frequency", "symbol", "left", "right"])):
    def __lt__(self, other):
        return self.frequency < other.frequency

def load_code_table(f):

    ext_length = int.from_bytes(f.read(1), 'big')
    file_extension = f.read(ext_length).decode()

    code_table = {}
    num_symbols = int.from_bytes(f.read(4), 'big')
    for _ in range(num_symbols):
        symbol = int.from_bytes(f.read(1), 'big')
        code_length = int.from_bytes(f.read(1), 'big')
        code_bytes = f.read((code_length + 7) // 8)
        code = bin(int.from_bytes(code_bytes, 'big'))[2:].zfill(code_length)
        code_table[code] = symbol

    return file_extension, code_table


def decompress_data(binary_data, code_table):
    result = bytearray()
    code = ""
    for bit in binary_data:
        code += bit
        if code in code_table:
            result.append(code_table[code])
            code = ""
    return result


def compress_file(file_path):
    data = read_file(file_path)
    file_extension = os.path.splitext(file_path)[1][1:]  # Extract extension without dot
    frequency_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)
    code_table = build_huffman_codes(huffman_tree)
    compressed_data = compress_data(data, code_table)
    compressed_file_path = os.path.splitext(file_path)[0] + ".bin"  # Save as .bin file
    save_compressed_file(compressed_file_path, compressed_data, code_table, file_extension)
    print(f"Файл сжат и сохранен как {compressed_file_path}")
    return compressed_file_path

def decompress_file(file_path):
    with open(file_path, "rb") as f:
        file_extension, code_table = load_code_table(f)
        padding_length = int.from_bytes(f.read(1), 'big')
        compressed_data_length = int.from_bytes(f.read(4), 'big')
        compressed_data = f.read()

        # Convert bytes to binary string, then truncate padding
        binary_data = ''.join(f'{byte:08b}' for byte in compressed_data)
        binary_data = binary_data[:compressed_data_length - padding_length]

        decompressed_data = decompress_data(binary_data, code_table)

    decompressed_file_path = file_path.replace(".bin", f"_decompressed.{file_extension}")
    with open(decompressed_file_path, "wb") as f:
        f.write(decompressed_data)
    print(f"Файл расшифрован и сохранен как {decompressed_file_path}")


def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


if __name__ == "__main__":
    import time

    name = input('Имя файла: ')
    name_bin = os.path.splitext(name)[0]
    original_size = os.path.getsize(name)
    start_time = time.time()
    path_bin = compress_file(name)
    end_time = time.time() - start_time
    compressed_size = os.path.getsize(path_bin)
    compression_ratio = original_size / compressed_size

    if compressed_size >= original_size:
        efficiency = 0
    else:
        efficiency = (1 - compressed_size / original_size) * 100

    print(f"Исходный размер: {original_size} байт")
    print(f"Закодированный размер: {compressed_size} байт")
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")
    print(f"Относительная эффективность: {efficiency:.2f}%")
    print(f"Время за которое выполнялась программа: {end_time} секунд")

    decompress_file(f"{name_bin}.bin")
