def fixed_length_encode(data, num_bits=8):
    encoded_msg = ''.join([format(ord(char), f'0{num_bits}b') for char in data])
    return encoded_msg


def fixed_length_decode(encoded, num_bits=8):
    decoded = [chr(int(encoded[i:i + num_bits], 2)
                   ) for i in range(0, len(encoded), num_bits)]
    return ''.join(decoded)


if __name__ == '__main__':
    from main import evaluate_compression
    import time

    start_time = time.time()
    # Пример использования
    with open('text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    encoded_text = fixed_length_encode(text, num_bits=16)
    with open('encoded_text_Fixed.txt', 'w', encoding='utf-8') as w:
        w.write(encoded_text)
    decoded_text = fixed_length_decode(encoded_text, num_bits=16)
    with open('decoded_text_Fixed.txt', 'w', encoding='utf-8') as w:
        w.write(decoded_text)
    end_time = time.time() - start_time
    evaluate_compression(text, encoded_text, end_time)
