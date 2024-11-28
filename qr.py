import qrcode
from PIL import Image, ImageDraw
import random
import os


def generate_qr(text, fill_color="black", back_color="white"):
    """Создает базовый QR-код с высоким уровнем коррекции ошибок."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(text)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")


def add_black_square(image, position, scale=0.3):
    """Добавляет черный квадрат в указанную позицию."""
    draw = ImageDraw.Draw(image)
    width, height = image.size
    square_size = int(min(width, height) * scale)
    if position == "center":
        x = (width - square_size) // 2
        y = (height - square_size) // 2
    elif position == "top-left":
        x, y = 0, 0
    elif position == "top-right":
        x, y = width - square_size, 0
    elif position == "bottom-left":
        x, y = 0, height - square_size
    elif position == "bottom-right":
        x, y = width - square_size, height - square_size
    else:
        return image

    draw.rectangle([(x, y), (x + square_size, y + square_size)], fill="black")
    return image


def add_pixel_noise(image, level):
    """Добавляет сильный шум в QR-код (меняет пиксели)."""
    pixels = image.load()
    width, height = image.size
    for _ in range(level):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        current_color = pixels[x, y]
        if current_color == (0, 0, 0):  # Черный пиксель
            pixels[x, y] = (255, 255, 255)  # Белый
        elif current_color == (255, 255, 255):  # Белый пиксель
            pixels[x, y] = (0, 0, 0)  # Черный
    return image


def generate_color_variants(image):
    """Создает цветные варианты QR-кода."""
    width, height = image.size
    pixels = image.load()
    variants = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Красный, зеленый, синий
    for color in colors:
        img = Image.new("RGB", (width, height), "white")
        img_pixels = img.load()
        for x in range(width):
            for y in range(height):
                if pixels[x, y] == (0, 0, 0):  # Черный пиксель
                    img_pixels[x, y] = color
        variants.append(img)
    return variants


def save_images(images, output_dir, base_name):
    """Сохраняет изображения с уникальными именами."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, img in enumerate(images):
        img.save(os.path.join(output_dir, f"{base_name}_{i + 1}.png"))


def main():
    text = input("Введите текст для QR-кода: ")
    output_dir = input("Введите имя папки для сохранения (например, qr_codes): ")

    # Базовый QR-код
    qr_base = generate_qr(text)

    # Модификации
    images = []

    # Черные квадраты с увеличенными размерами
    for position in ["center", "top-left", "top-right", "bottom-left", "bottom-right"]:
        img = qr_base.copy()
        images.append(add_black_square(img, position, scale=0.4))  # Увеличен размер квадратов

    # QR-коды с сильным шумом
    noise_levels = [2000, 5000, 50000]  # Усиленный шум
    for level in noise_levels:
        img = qr_base.copy()
        images.append(add_pixel_noise(img, level))

    # Цветные QR-коды
    images.extend(generate_color_variants(qr_base))

    # Сохранение изображений
    save_images(images, output_dir, "qr_code")
    print(f"QR-коды сохранены в папке {output_dir}")


if __name__ == "__main__":
    main()
