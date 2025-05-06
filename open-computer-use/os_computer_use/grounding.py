from PIL import ImageDraw
import re


def draw_big_dot(image, coordinates, color="red", radius=12):
    draw = ImageDraw.Draw(image)
    x, y = coordinates
    bounding_box = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bounding_box, fill=color, outline=color)
    return image


def extract_bbox_midpoint(bbox_response):
    match = re.search(r"<\|box_start\|>(.*?)<\|box_end\|>", bbox_response)
    inner_text = match.group(1) if match else bbox_response
    numbers = [float(num) for num in re.findall(r"\d+\.\d+|\d+", inner_text)]
    if len(numbers) == 2:
        return numbers[0], numbers[1]
    elif len(numbers) >= 4:
        return (numbers[0] + numbers[2]) // 2, (numbers[1] + numbers[3]) // 2
    else:
        return None
