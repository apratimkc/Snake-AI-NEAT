"""
Command-line interface to CairoSVG.

"""

import argparse
import os
import sys

from . import SURFACES, VERSION


def main(argv=None, stdout=None, stdin=None):
    """Entry-point of the executable."""
    # Get command-line options
    parser = argparse.ArgumentParser(
        description='Convert SVG files to other formats')
    parser.add_argument('input', default='-', help='input filename or URL')
    parser.add_argument(
        '-v', '--version', action='version', version=VERSION)
    parser.add_argument(
        '-f', '--format', help='output format',
        choices=sorted([surface.lower() for surface in SURFACES]))
    parser.add_argument(
        '-d', '--dpi', default=96, type=float,
        help='ratio between 1 inch and 1 pixel')
    parser.add_argument(
        '-W', '--width', default=None, type=float,
        help='width of the parent container in pixels')
    parser.add_argument(
        '-H', '--height', default=None, type=float,
        help='height of the parent container in pixels')
    parser.add_argument(
        '-s', '--scale', default=1, type=float, help='output scaling factor')
    parser.add_argument(
        '-b', '--background', metavar='COLOR', help='output background color')
    parser.add_argument(
        '-n', '--negate-colors', action='store_true',
        help='replace every vector color with its complement')
    parser.add_argument(
        '-i', '--invert-images', action='store_true',
        help='replace every raster pixel with its complementary color')
    parser.add_argument(
        '-u', '--unsafe', action='store_true',
        help='resolve XML entities and allow very large files '
             '(WARNING: vulnerable to XXE attacks and various DoS)')
    parser.add_argument(
        '--output-width', default=None, type=float,
        help='desired output width in pixels')
    parser.add_argument(
        '--output-height', default=None, type=float,
        help='desired output height in pixels')

    parser.add_argument('-o', '--output', default='-', help='output filename')

    options = parser.parse_args(argv)
    kwargs = {
        'parent_width': options.width, 'parent_height': options.height,
        'dpi': options.dpi, 'scale': options.scale, 'unsafe': options.unsafe,
        'background_color': options.background,
        'negate_colors': options.negate_colors,
        'invert_images': options.invert_images,
        'output_width': options.output_width,
        'output_height': options.output_height}
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    kwargs['write_to'] = (
        stdout.buffer if options.output == '-' else options.output)
    if options.input == '-':
        kwargs['file_obj'] = stdin.buffer
    else:
        kwargs['url'] = options.input
    output_format = (
        options.format or
        os.path.splitext(options.output)[1].lstrip('.') or
        'pdf').upper()

    SURFACES[output_format.upper()].convert(**kwargs)


if __name__ == '__main__':  # pragma: no cover
    main()
