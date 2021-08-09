"""ST7735 Display plugin for pidi."""
from ST7735 import ST7735 as ST7735, BG_SPI_CS_FRONT, ST7735_DISPOFF, ST7735_DISPON
from pidi_display_pil import DisplayPIL

__version__ = '0.1.0'


class DisplayST7735(DisplayPIL):
    """pidi display output plugin for the ST7735 1.77\" 128x160 SPI LCD"""

    option_name = 'st7735'

    def __init__(self, args):
        DisplayPIL.__init__(self, args)
        self._st7735 = ST7735(
            rotation=args.rotation,
            port=args.spi_port,
            cs=args.spi_chip_select_pin,
            dc=args.spi_data_command_pin,
            backlight=args.backlight_pin,
            spi_speed_hz=args.spi_speed_mhz * 1000 * 1000
        )
        self._st7735.begin()

    def start(self):
        self._st7735.command(ST7735_DISPON)
        self._st7735.set_backlight(100)

    def stop(self):
        self._st7735.set_backlight(0)
        self._st7735.command(ST7735_DISPOFF)

    def redraw(self):
        if DisplayPIL.redraw(self):
            self._st7735.display(self._output_image)

    def add_args(argparse):
        """Add supplemental arguments for ST7735."""
        DisplayPIL.add_args(argparse)

        argparse.add_argument("--rotation",
                              help="Rotation in degrees (Default: 90)",
                              type=int, default=90, choices=[0, 90, 180, 270])
        argparse.add_argument("--spi-port",
                              help="SPI port (Default 0)",
                              type=int, default=0, choices=[0, 1])
        argparse.add_argument("--spi-chip-select-pin",
                              help="SPI chip select (Default 1)",
                              type=int, default=1, choices=[0, 1])
        argparse.add_argument("--spi-data-command-pin",
                              help="SPI data/command pin (Default 9)",
                              type=int, default=9)
        argparse.add_argument("--spi-speed-mhz",
                              help="SPI speed in Mhz (Default 80)",
                              type=int, default=80)
        argparse.add_argument("--backlight-pin",
                              help="ST7735 backlight pin (Default 13)",
                              type=int, default=13)
