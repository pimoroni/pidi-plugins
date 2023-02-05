"""ST7789 Display plugin for pidi."""
from OrangePi import ST7789, ST7789_DISPOFF, ST7789_DISPON
from OrangePi_PidiPlugins import DisplayPIL

__version__ = '1.0.0'

class DisplayST7789(DisplayPIL):
    """pidi display output plugin for the ST7789 SPI LCD"""

    option_name = 'opi.st7789'

    def __init__(self, args):
        DisplayPIL.__init__(self, args)
        self._st7789 = ST7789(
            rotation=args.rotation,
            port=args.spi_port,
            cs=args.spi_chip_select_pin,
            dc=args.spi_data_command_pin,
            rst=args.spi_reset_pin,
            backlight=args.backlight_pin,
            width=args.width,
            height=args.height,
            spi_speed_hz=args.spi_speed_mhz * 1000 * 1000
        )
        self._st7789.begin()

    def start(self):
        self._st7789.command(ST7789_DISPON)
        self._st7789.set_backlight(100)

    def stop(self):
        self._st7789.set_backlight(0)
        self._st7789.command(ST7789_DISPOFF)

    def redraw(self):
        if DisplayPIL.redraw(self):
            self._st7789.display(self._output_image)

    def add_args(argparse):
        """Add supplemental arguments for ST7789."""
        DisplayPIL.add_args(argparse)

        argparse.add_argument("--rotation",
                              help="Rotation in degrees (Default: 0)",
                              type=int, default=0, choices=[0, 90, 180, 270])
        argparse.add_argument("--spi-port",
                              help="SPI port (Default 0)",
                              type=int, default=0, choices=[0, 1])
        argparse.add_argument("--spi-chip-select-pin",
                              help="SPI chip select (Default 0)",
                              type=int, default=0, choices=[0, 1])
        argparse.add_argument("--spi-data-command-pin",
                              help="SPI data/command pin (Default 27)",
                              type=int, default=27)
        argparse.add_argument("--spi-reset-pin",
                              help="SPI reset pin (Default 17)",
                              type=int, default=17)
        argparse.add_argument("--width",
                              help="LCD width, default 320",
                              type=int, default=320)
        argparse.add_argument("--height",
                              help="LCD height, default 240",
                              type=int, default=240)
        argparse.add_argument("--spi-speed-mhz",
                              help="SPI speed in Mhz (Default 80)",
                              type=int, default=80)
        argparse.add_argument("--backlight-pin",
                              help="ST7789 backlight pin (Default 22)",
                              type=int, default=22)
