from urllib.parse import urlparse
import argparse
import os
import png
import pyqrcode


class InvalidFileTypeException(Exception):
    """ Raised when output_type is not PNG or SVG """


def get_hostname_from_url(url: str) -> str:
    return urlparse(url).hostname


def bulk_url_to_qr(urls_file: str, output_type: str) -> None:
    with open(urls_file) as file:
        print("[*] Creating directory qr_codes.")
        os.mkdir('qr_codes')

        for url in file:
            path = "qr_codes/" + get_hostname_from_url(url)
            url_to_qr_code(url.rstrip('\n'), output_type, path)


def url_to_qr_code(url: str, output_type: str, filename=None) -> None:
    qr_code = pyqrcode.create(url)

    if not filename:
        filename = get_hostname_from_url(url)

    if output_type.lower() == "png":
        qr_code.png(filename + ".png", scale=8)
    elif output_type.lower() == "svg":
        qr_code.svg(filename + ".svg", scale=8)
    else:
        raise InvalidFileTypeException("Output file type must be PNG or SVG.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create QR codes from a from a file "
                                                 "with a list of URLs or for a single URL.")
    # Mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file",
                       dest="urls_file",
                       help="File with a list of URLs.")
    group.add_argument("-u", "--url",
                       dest="url",
                       help="URL to convert to QR code.")
    # End of Mutually exclusive group

    parser.add_argument("-t", "--output-type",
                        dest="output_type",
                        required=True,
                        choices=["png", "svg"],
                        help="Output type of the QR code image.")
    parser.add_argument("-o", "--output-filename",
                        dest="filename",
                        default=None,
                        help="Output name of the created QR code image.")

    args = parser.parse_args()

    if args.urls_file is not None:
        if os.path.exists(args.urls_file):
            bulk_url_to_qr(args.urls_file, args.output_type)
        else:
            raise FileNotFoundError(f"{args.urls_file} does not exists.")
    elif args.url is not None:
        url_to_qr_code(args.url, args.output_type, args.filename)


if __name__ == "__main__":
    main()

