
# Узел дерева Хаффмана
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Построение дерева Хаффмана
def build_huffman_tree(text):
    frequency = Counter(text)
    print(frequency)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


# Создание кодов для каждого символа
def build_codes(node, prefix="", codebook={}):
    if node is None:
        return
    if node.char is not None:
        codebook[node.char] = prefix
    build_codes(node.left, prefix + "0", codebook)
    build_codes(node.right, prefix + "1", codebook)
    return codebook


# Кодирование текста
def huffman_encode(text, codebook):
    return ''.join(codebook[char] for char in text)


# Декодирование текста
def huffman_decode(encoded_text, tree):
    decoded_text = []
    node = tree
    for bit in encoded_text:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.left is None and node.right is None:
            decoded_text.append(node.char)
            node = tree
    return ''.join(decoded_text)


def print_huffman_tree(node, prefix=""):
    if node is None:
        return

    # Если узел является листом (имеет символ)
    if node.char is not None:
        print(f"{prefix}└─({node.char}:{node.freq})")
    else:
        # Узел не является листом, печатаем частоту
        print(f"{prefix}├─({node.freq})")

    # Рекурсивно печатаем левое и правое поддерево с отступом
    if node.left is not None:
        print_huffman_tree(node.left, prefix + "   ")
    if node.right is not None:
        print_huffman_tree(node.right, prefix + "   ")


# Функция для оценки эффективности
def evaluate_compression(original_text, encod_text, time_foo = None, cbook=None, treePr=None):
    if treePr:
        print_huffman_tree(treePr)
    if cbook:
        print(cbook)
    original_size = len(original_text) * 8

    compressed_size = len(encod_text)

    compression_ratio = original_size / compressed_size

    efficiency = (1 - compressed_size / original_size) * 100

    print(f"Исходный размер: {original_size} бит")
    print(f"Закодированный размер: {compressed_size} бит")
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")
    print(f"Относительная эффективность: {efficiency:.2f}%")
    print(f"Время за которое выполнялась программа: {time_foo} секунд")

def main():
    try:
        with open('text.txt', 'r', encoding='utf-8') as f:
            text = f.read()

        tree = build_huffman_tree(text)
        codebook = build_codes(tree)

        encoded_text = huffman_encode(text, codebook)

        with open('encoded_text.txt', 'w', encoding='utf-8') as w:
            w.write(encoded_text)

        decoded_text = huffman_decode(encoded_text, tree)
        with open('decoded_text.txt', 'w', encoding='utf-8') as w:
            w.write(decoded_text)
        return text, encoded_text, codebook, tree

    except Exception as e:
        print(e)


if __name__ == '__main__':
    import heapq
    from collections import Counter
    import time
    start_t = time.time()
    text, encoded_text, codebook, tree = main()
    end_time = time.time() - start_t
    evaluate_compression(text, encoded_text, end_time, codebook, tree)
