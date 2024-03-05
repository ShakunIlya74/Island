from PIL import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Python310\Lib\site-packages\pytesseract\pytesseract.py'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def get_pixel_color(image_path, x, y):
    try:
        # Open the image
        image = Image.open(image_path)

        # Get the RGB values of the pixel at given coordinates
        pixel_color = image.getpixel((x, y))

        return pixel_color
    except Exception as e:
        print(f"Error: {e}")
        return None


def retrieve_text_from_image(image_path):
    # Timeout/terminate the tesseract job after a period of time
    try:
        output = pytesseract.image_to_string(image_path, timeout=2)  # Timeout after 2 seconds
        # print(output)
        return output
        # print(pytesseract.image_to_string('test.jpg', timeout=0.5))  # Timeout after half a second
    except RuntimeError as timeout_error:
        # Tesseract processing is terminated
        return ''


if __name__ == '__main__':
    image_path = "../data/screenshots/temp_screen.png"
    # x_coordinate = 750
    # y_coordinate = 530
    # pixel_color = get_pixel_color(image_path, x_coordinate, y_coordinate)
    # print(f"RGB color at coordinates ({x_coordinate}, {y_coordinate}): {pixel_color}")

    text = retrieve_text_from_image(image_path)
    print(text)