"""pidi plugin for Tk display."""
import time
import math
import os

try:
    from pidi.display import Display
except ImportError:
    from mopidy_pidi.plugin import Display


__version__ = '0.1.0'


def text_in_rect(canvas, text, font, rect, line_spacing=1.1):
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


def draw_progress_bar(canvas, progress, max_progress, rect, colour):
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

        source_size = (self._size * self._downscale, self._size * self._downscale)
        target_size = (self._size, self._size)

        self._image_album_art = Image.new('RGBA', target_size , (0, 0, 0))
        self._image_album_art_prev = Image.new('RGBA', target_size, (0, 0, 0))

        self._text = Image.new('RGBA', source_size)
        self._text_draw = ImageDraw.Draw(self._text, 'RGBA')
        self._text_draw.fontmode = '1'
        self._text_1x = None

        self._overlay = Image.new('RGBA', target_size)
        self._overlay_draw = ImageDraw.Draw(self._overlay, 'RGBA')

        self._output_image = None
        self._last_art_change = time.time()
        self._blur = args.blur_album_art

        self._image_dir = os.path.join(os.path.dirname(__file__), "images")
        self.controls_pause = Image.open(
                os.path.join(self._image_dir, "controls-pause.png")).resize(target_size, resample=Image.LANCZOS).convert("RGBA")
        self.controls_play = Image.open(
                os.path.join(self._image_dir, "controls-play.png")).resize(target_size, resample=Image.LANCZOS).convert("RGBA")

        self._last_artist = ""
        self._last_title = ""
        self._last_album = ""
        self._last_state = ""
        self._last_volume = -1
        self._last_progress = -1

    def update_album_art(self, input_file):
        # Save the old album art
        self._image_album_art_prev.paste(self._image_album_art, (0, 0))

        # Prepare the new album art
        new = Image.open(input_file).resize((self._size * self._downscale, self._size * self._downscale))
        if self._blur:
            new = new.convert('RGBA').filter(ImageFilter.GaussianBlur(radius=5*self._downscale))
        new = new.resize((self._size, self._size), resample=Image.LANCZOS)
        self._image_album_art.paste(new, (0, 0))
        self._last_art_change = time.time()

    def update_overlay(self, *args):
        Display.update_overlay(self, *args)

        if (self._last_title, self._last_artist, self._last_album) != (self._title, self._artist, self._album):
            self.update_text_layer()
            self._last_title = self._title
            self._last_artist = self._artist
            self._last_album = self._album

    def update_text_layer(self):
        self._text_draw.rectangle((0, 0, self._size * self._downscale, self._size * self._downscale), (0, 0, 0, 0))

        margin = 5
        width = self._size * self._downscale

        # Artist
        artist = self._artist

        if ";" in artist:
            artist = artist.replace(";", ", ")  # Swap out weird semicolons for commas

        box = text_in_rect(self._text_draw, artist, self._font_medium, (margin, 5 * self._downscale, width - margin, 35 * self._downscale))

        # Album
        text_in_rect(self._text_draw, self._album, self._font_small, (50 * self._downscale, box[3], width - (50 * self._downscale), 70 * self._downscale))

        # Song title
        text_in_rect(self._text_draw, self._title, self._font, (margin, 95 * self._downscale, width - margin, 170 * self._downscale))

        # Downscale track information
        self._text_1x = self._text.resize((int(width / self._downscale), int(width / self._downscale)), resample=Image.LANCZOS)

    def redraw(self):
        margin = 5

        t_blend = min(0.25, time.time() - self._last_art_change)
        t_blend *= 4

        # We don't want to update on every millisecond of progress,
        # only when it happens to cross to the next pixel on the display
        # and trigger a visual change
        progress_pixels = int(self._progress * (self._size - margin - margin))

        if self._output_image is not None \
                and t_blend == 1.0 \
                and self._state == self._last_state \
                and self._volume == self._last_volume \
                and self._last_progress == progress_pixels:
            return False  # No change since last frame

        self._last_state = self._state
        self._last_volume = self._volume
        self._last_progress = progress_pixels
        self._last_redraw = time.time()

        # Initial setup
        self._overlay_draw.rectangle((0, 0, self._size, self._size), (0, 0, 0, 40))

        # Song progress bar
        progress = self._progress
        max_progress = 1.0
        colour = (225, 225, 225, 225)
        rect = (5, 220, 235, 235)
        draw_progress_bar(self._overlay_draw, progress, max_progress, rect, colour)

        # Volume bar
        volume = self._volume
        max_volume = 100
        colour = (225, 225, 225, 165)
        rect = (5, 185, 205, 190)
        draw_progress_bar(self._overlay_draw, volume, max_volume, rect, colour)

        # Crossfade Album Art
        if t_blend == 1.0:
            art = self._image_album_art
        else:
            art = Image.blend(self._image_album_art_prev, self._image_album_art, t_blend)

        # Add our text layer
        if self._text_1x is not None:
            overlay = Image.alpha_composite(self._overlay, self._text_1x)
        else:
            overlay = self._overlay

        # Overlay control icons
        if self._state == "play":
            overlay = Image.alpha_composite(overlay, self.controls_play)
        else:
            overlay = Image.alpha_composite(overlay, self.controls_pause)

        # Overlay combined track info onto album art
        image = Image.alpha_composite(art, overlay)

        self._output_image = image
        return True

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
                              default="pidi-output.png")

    def redraw(self):
        DisplayPIL.redraw(self)
        self._output_image.save(self._output_file, "PNG")
