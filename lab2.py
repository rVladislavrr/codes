class GaloisField:
    def __init__(self, field_size, primitive_polynomial):
        self.field_size = field_size
        self.primitive_polynomial = primitive_polynomial
        self.alpha = 2
        self.generate_tables()

    def generate_tables(self):
        self.exp_table = [1] * (self.field_size * 2)
        self.log_table = [0] * self.field_size
        x = 1
        for i in range(self.field_size - 1):
            self.exp_table[i] = x
            self.log_table[x] = i
            x = self.mul(x, self.alpha)
        for i in range(self.field_size - 1, self.field_size * 2 - 1):
            self.exp_table[i] = self.exp_table[i - (self.field_size - 1)]

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp_table[(self.log_table[a] + self.log_table[b]) % (self.field_size - 1)]

    def div(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        if a == 0:
            return 0
        return self.exp_table[(self.log_table[a] - self.log_table[b]) % (self.field_size - 1)]

    def add(self, a, b):
        return a ^ b

    def evaluate_polynomial(self, poly, x):
        result = 0
        for coeff in poly:
            result = self.add(result, self.mul(coeff, x))
        return result


class ReedSolomon:
    def __init__(self, n, k, field):
        self.n = n
        self.k = k
        self.t = (n - k) // 2
        self.field = field

    def encode(self, message):
        message_poly = [ord(c) for c in message] + [0] * (self.n - len(message))
        generator_poly = self.generator_polynomial()
        encoded = self.polynomial_division(message_poly, generator_poly)[1]
        return message_poly + encoded

    def generator_polynomial(self):
        g = [1]
        for i in range(self.t):
            g = self.polynomial_multiply(g, [1, self.field.alpha ** (i)])
        return g

    def polynomial_multiply(self, poly1, poly2):
        result = [0] * (len(poly1) + len(poly2) - 1)
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                result[i + j] = self.field.add(result[i + j], self.field.mul(poly1[i], poly2[j]))
        return result

    def polynomial_division(self, dividend, divisor):
        remainder = dividend[:]
        while len(remainder) >= len(divisor):
            factor = self.field.div(remainder[0], divisor[0])
            for i in range(len(divisor)):
                remainder[i] = self.field.add(remainder[i], self.field.mul(factor, divisor[i]))
            remainder = remainder[1:]
        return divisor, remainder

    def decode(self, received):
        syndromes = self.compute_syndromes(received)
        if all(s == 0 for s in syndromes):
            return ''.join(chr(c) for c in received[:self.k])


        error_locator, error_positions = self.find_errors(syndromes)

        # Исправление ошибок
        corrected_message = received[:]
        for pos in error_positions:
            corrected_message[pos] = self.field.add(corrected_message[pos], 1)  # Простейшее исправление ошибки
        return ''.join(chr(c) for c in corrected_message[:self.k])

    def compute_syndromes(self, received):
        syndromes = []
        for i in range(self.t):
            syndrome = 0
            for j in range(self.n):
                power = (i * j) % (self.field.field_size - 1)
                syndrome = self.field.add(syndrome, self.field.mul(received[j], self.field.alpha ** power))
            syndromes.append(syndrome)
        return syndromes

    def find_errors(self, syndromes):
        error_locator = [1]
        for i in range(len(syndromes)):
            delta = syndromes[i]
            for j in range(1, len(error_locator)):
                delta ^= self.field.mul(error_locator[-(j + 1)], syndromes[i - j])
            if delta != 0:
                error_locator.append(delta)
        error_positions = [i for i in range(self.n) if
                           self.field.evaluate_polynomial(error_locator, self.field.alpha ** i) == 0]
        return error_locator, error_positions


def main():

    field = GaloisField(256, 0x11d)  # Поле GF(256) с примитивным многочленом 0x11d (x^8 + x^4 + x^3 + x + 1)
    message = input("Введите строку для кодирования: ")
    k = len(message)
    n = 2 * k
    rs = ReedSolomon(n, k, field)

    encoded = rs.encode(message)
    print("Зашифрованное сообщение:", encoded)

    encoded_with_error = encoded[:]
    encoded_with_error[5] ^= 1

    print("Сообщение с ошибкой:", encoded_with_error)

    decoded = rs.decode(encoded_with_error)
    print("Расшифрованное сообщение:", decoded)


if __name__ == "__main__":
    main()
