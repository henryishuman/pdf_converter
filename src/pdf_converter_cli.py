from typing import List

from pdf_converter import PDFConverter
from sys import argv
from os.path import splitext

options = [
    "-in", "-out", "-ext"
]

def cli_help():
    print("1. Convert a PDF to a PNG file of the same name:")
    print("`python pdf_converter_cli.py convert [input_filename]`")
    print()
    print("2. Convert a PDF to a PNG file of the same name:")
    print("`python pdf_converter_cli.py convert -in [input_filename]`")
    print()
    print("3. Convert a PDF to an image file of the same name and given extension:")
    print("`python pdf_converter_cli.py convert -in [input_filename] -ext [extension]`")
    print()
    print("4. Convert a PDF to an image file of a given name:")
    print("`python pdf_converter_cli.py convert -in [input_filename] -out [output_filename]`")
    print()

def get_write_path(from_file: str, to_file: str, extension: str):
    if from_file is None:
        raise ValueError(f"Please supply a valid file path")

    if to_file is not None:
        root, has_extension = splitext(to_file)
        if has_extension:
            to_file_extension = to_file.split(".")[-1]
            extension = to_file_extension
            to_file = to_file.replace("." + to_file_extension, "")
    else:
        to_file = from_file.replace(".pdf", "")

    if extension is None:
        extension = ".png"
    if "." not in extension:
        extension = "." + extension

    return to_file + extension

def cli_convert_to_image(from_file: str, to_file: str, extension: str):
    write_path = get_write_path(from_file, to_file, extension)
    converter = PDFConverter(from_file)
    converter.save_as_image(write_path)

def get_option_key_value_pairs(args: List[str]):
    option_key_value_pairs = {}
    options_provided = False
    for option in options:
        if option in args:
            options_provided = True
            option_key_value_pairs[option] = args[args.index(option) + 1]
        else:
            option_key_value_pairs[option] = None

    if not options_provided and not option_key_value_pairs["-in"] and len(args) > 2:
        option_key_value_pairs["-in"] = args[2]
    if not options_provided and not option_key_value_pairs["-out"] and len(args) > 3:
        option_key_value_pairs["-out"] = args[3]

    return option_key_value_pairs

def pdf_converter_cli(args: List[str]):
    if args[1] == "help":
        cli_help()
    elif args[1] == "convert":
        option_key_value_pairs = get_option_key_value_pairs(args)
        cli_convert_to_image(
            from_file=option_key_value_pairs["-in"],
            to_file=option_key_value_pairs["-out"],
            extension=option_key_value_pairs["-ext"])
    else:
        raise ValueError(f"Command `{args[1]}` not recognised. Please consult the README or use the help command for more")

if __name__ == "__main__":
    pdf_converter_cli(argv)