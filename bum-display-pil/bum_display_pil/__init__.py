"""bum plugin for Tk display."""
import time
import math
import os

try:
    from bum.display import Display
except ImportError:
    from mopidy_pirate_display.plugin import Display


__version__ = '0.0.1'


def text_in_rect(image, text, font, rect, line_spacing=1.1):
    canvas = ImageDraw.Draw(image, 'RGBA')

    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    # Given a rectangle, reflow and scale text to fit, centred
    while font.size > 0:
        space_width = font.getsize(" ")[0]
        line_height = int(font.size * line_spacing)
        max_lines = math.floor(height / line_height)
        lines = []

        # Determine if text can fit at current scale.
        words = text.split(" ")

        while len(lines) < max_lines and len(words) > 0:
            line = []

            while len(words) > 0 and font.getsize(" ".join(line + [words[0]]))[0] <= width:
                line.append(words.pop(0))

            lines.append(" ".join(line))

        if(len(lines)) <= max_lines and len(words) == 0:
            # Solution is found, render the text.
            y = int(rect[1] + (height / 2) - (len(lines) * line_height / 2) - (line_height - font.size) / 2)

            bounds = [rect[2], y, rect[0], y + len(lines) * line_height]

            for line in lines:
                line_width = font.getsize(line)[0]
                x = int(rect[0] + (width / 2) - (line_width / 2))
                bounds[0] = min(bounds[0], x)
                bounds[2] = max(bounds[2], x + line_width)
                canvas.text((x, y), line, font=font)
                y += line_height

            return tuple(bounds)

        font = ImageFont.truetype(font.path, font.size - 1)


def draw_progress_bar(image, progress, max_progress, rect, colour):
    canvas = ImageDraw.Draw(image, 'RGBA')

    unfilled_opacity = 0.5  # Factor to scale down colour/opacity of unfilled bar.

    # Calculate bar widths.
    rect = tuple(rect)  # Space which bar occupies.
    full_width = rect[2] - rect[0]
    bar_width = int((progress / max_progress) * full_width)
    progress_rect = (rect[0], rect[1], rect[0] + bar_width, rect[3])

    # Knock back unfilled part of bar.
    unfilled_colour = tuple(int(c * unfilled_opacity) for c in colour)

    # Draw bars.
    canvas.rectangle(rect, unfilled_colour)
    canvas.rectangle(progress_rect, colour)


class DisplayPIL(Display):
    """Base class for PIL-based image displays."""
    def __init__(self, args=None):
        global Image, ImageDraw, ImageFilter, ImageFont, ConnectionIII

        Display.__init__(self, args)

        from fonts.ttf import RobotoMedium as UserFont
        from PIL import Image, ImageDraw, ImageFilter, ImageFont

        self._downscale = 2
        self._font = ImageFont.truetype(UserFont, 42 * self._downscale)
        self._font_small = ImageFont.truetype(UserFont, 20 * self._downscale)
        self._font_medium = ImageFont.truetype(UserFont, 25 * self._downscale)

        self._image = Image.new('RGBA', (self._size * self._downscale, self._size * self._downscale), (0, 0, 0))
        self._overlay = Image.new('RGBA', (self._size * self._downscale, self._size * self._downscale))
        self._draw = ImageDraw.Draw(self._overlay, 'RGBA')
        self._draw.fontmode = '1'
        self._output_image = None
        self._last_change = time.time()
        self._blur = args.blur_album_art

    def update_album_art(self, input_file):
        new = Image.open(input_file).resize((self._size * self._downscale, self._size * self._downscale))
        if self._blur:
            new = new.convert('RGBA').filter(ImageFilter.GaussianBlur(radius=5*self._downscale))
        self._image.paste(new, (0, 0))
        self._last_change = time.time()

    def redraw(self):
        # Initial setup
        self._draw.rectangle((0, 0, self._size * self._downscale, self._size * self._downscale), (0, 0, 0, 40))
        margin = 5
        width = self._size * self._downscale

        # Song progress bar
        progress = self._progress
        max_progress = 1.0
        colour = (225, 225, 225, 225)
        rect = (5, 220, 235, 235)
        scaled_rect = (v * self._downscale for v in rect)
        draw_progress_bar(self._overlay, progress, max_progress, scaled_rect, colour)

        # Volume bar
        volume = self._volume
        max_volume = 100
        colour = (225, 225, 225, 165)
        rect = (5, 185, 205, 190)
        scaled_rect = (v * self._downscale for v in rect)
        draw_progress_bar(self._overlay, volume, max_volume, scaled_rect, colour)

        # Artist
        artist = self._artist

        if ";" in artist:
            artist = artist.replace(";", ", ")  # Swap out weird semicolons for commas

        box = text_in_rect(self._overlay, artist, self._font_medium, (margin, 5 * self._downscale, width - margin, 35 * self._downscale))

        # Album
        text_in_rect(self._overlay, self._album, self._font_small, (50 * self._downscale, box[3], width - (50 * self._downscale), 70 * self._downscale))

        # Song title
        text_in_rect(self._overlay, self._title, self._font, (margin, 95 * self._downscale, width - margin, 170 * self._downscale))

        # Overlay control icons
        image_dir = os.path.join(os.path.dirname(__file__), "images")
        controls = Image.new('RGBA', (self._size * self._downscale, self._size * self._downscale))

        if self._state == "play":
            controls_img = Image.open(os.path.join(image_dir, "controls-pause.png"))
        else:
            controls_img = Image.open(os.path.join(image_dir, "controls-play.png"))

        controls.paste(controls_img, (0, 0))

        # Render image
        image_2x = Image.alpha_composite(self._image, self._overlay)
        image_2x = Image.alpha_composite(image_2x, controls)
        image_1x = image_2x.resize((int(width / self._downscale), int(width / self._downscale)), resample=Image.LANCZOS)
        self._output_image = image_1x

    def add_args(argparse):
        Display.add_args(argparse)

        argparse.add_argument("--blur-album-art",
                              help="Apply blur effect to album art.",
                              action='store_true')


class DisplayFile(DisplayPIL):
    option_name = 'file'

    def __init__(self, args=None):
        DisplayPIL.__init__(self, args)
        self._output_file = args.output_file

    def add_args(argparse):
        DisplayPIL.add_args(argparse)

        argparse.add_argument("--output-file",
                              help="File to output display image.",
                              type=str,
                              default="bum-output.png")

    def redraw(self):
        DisplayPIL.redraw(self)
        self._output_image.save(self._output_file, "PNG")
