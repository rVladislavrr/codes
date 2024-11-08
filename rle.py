import os
import sys


def rle_compress(data):
    """Функция сжатия с использованием алгоритма RLE"""
    compressed = []
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        compressed.append((data[i], count))
        i += 1
    return compressed


def rle_decompress(compressed):
    """Функция распаковки сжатых данных с использованием алгоритма RLE"""
    decompressed = []
    for char, count in compressed:
        decompressed.append(char * count)
    return ''.join(decompressed)


def compress_file(file_path):
    """Функция сжатия файла с использованием алгоритма RLE"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        compressed_data = rle_compress(data)
        compressed_file_path = os.path.splitext(file_path)[0] +'rle.bin'
        with open(compressed_file_path, 'wb') as f:
            for char, count in compressed_data:
                # Преобразуем символ в байт и записываем его с количеством
                char_byte = char.encode('utf-8')  # Преобразуем символ в байты
                f.write(len(char_byte).to_bytes(1, byteorder='big'))  # Длина байтового представления символа
                f.write(char_byte)  # Записываем символ в виде байтов
                f.write(count.to_bytes(4, byteorder='big'))  # Записываем количество повторений

        print(f"Файл сжат и сохранен в {compressed_file_path}")
        return compressed_file_path

    except Exception as e:
        print(f"Ошибка при сжатии файла: {e}")
        sys.exit(1)


def decompress_file(compressed_file_path, output_path):
    """Функция распаковки сжатого файла"""
    try:
        with open(compressed_file_path, 'rb') as f:
            decompressed_data = []
            while True:
                length_byte = f.read(1)
                if not length_byte:
                    break
                length = int.from_bytes(length_byte, byteorder='big')
                char_bytes = f.read(length)
                if not char_bytes:
                    break
                char = char_bytes.decode('utf-8')  # Преобразуем байты в символ
                count_bytes = f.read(4)
                if not count_bytes:
                    break
                count = int.from_bytes(count_bytes, byteorder='big')
                decompressed_data.append(char * count)

            decompressed_str = ''.join(decompressed_data)
            output_path = os.path.splitext(output_path)[0] + '.txt'
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(decompressed_str)

        print(f"Файл распакован и сохранен в {output_path}")

    except Exception as e:
        print(f"Ошибка при распаковке файла: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import time
    input_file_path = input("Введите путь к файлу для сжатия: ")

    if not os.path.exists(input_file_path):
        print("Файл не существует.")
        sys.exit(1)
    original_size = os.path.getsize(input_file_path)
    start_time = time.time()
    compressed_file_path = compress_file(input_file_path)
    end_time = time.time() - start_time
    compressed_size = os.path.getsize(compressed_file_path)
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



    output_file_path = input("Введите путь для распаковки файла: ")

    decompress_file(compressed_file_path, output_file_path)
