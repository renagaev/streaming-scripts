from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont, ImageOps


class ButtonBase(ABC):
    def __init__(self):
        self.on_image_change = lambda x: 0
        self.image = None
        self._image = None
        self.image_changed = False

    @property
    def image(self):
        self.image_changed = False
        return self._image

    @image.setter
    def image(self, value):
        self.on_image_change(value)
        self.image_changed = True
        self._image = value

    @abstractmethod
    def on_press(self):
        pass

    def _create_image(self, color="black"):
        return Image.new("RGB", (72, 72), color)

    def render_text(self, text, color, fontsize):
        image = self._create_image(color)
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("C:/Users/Admin/Documents/vMixStorage/python/OpenSans-Regular.ttf", fontsize)
        label_w, label_h = draw.textsize(text, font=font)
        label_pos = ((image.width - label_w) // 2, (image.height - label_h) // 2 - 1)
        draw.text(label_pos, text=text, font=font, fill="white")
        return image

    def render_icon(self, icon, color="black"):
        image = self._create_image(color)
        icon = Image.open(f"C:/Users/Admin/PycharmProjects/stream/icons/{icon}.png")
        icon.thumbnail((45, 45), Image.LANCZOS)
        r, g, b, a = icon.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        icon = Image.merge('RGBA', (r2, g2, b2, a))
        icon_pos = ((image.width - icon.width) // 2, (image.height - icon.height) // 2)
        image.paste(icon, icon_pos, icon)
        return image
