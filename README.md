# READ ME
A wrapper surrounding the `PyMuPDF` and `fitz` packages. 
Converts PDFs to any image file type.

## Installation
Before running, please ensure to run the install script. 
This implementation relies on the `PyMuPDF` and `Pillow` 
packages which are not installed by default. 

To install, please run the following command from the 
project directory:

`pip install -r requirements.txt`

## How to use

### Standard functionality
To convert a PDF document to an image, run the following command:

`python ./pdf_converter_cli.py convert path/to/pdf_file.pdf`

By default, this will convert the PDF document to a PNG image with an identical name.

If you wish to supply a name for this output file, then you may do so with the following command:

`python ./pdf_converter_cli.py convert path/to/input_file.pdf path/to/output_file.png`

Excluding an extension from the output path will create a PNG file by default.

### Using argument tags
You can also run the program by supplying argument tags, for example:

`python ./pdf_converter_cli.py convert -in path/to/input_file.pdf -out path/to/output_file.png -ext .file_extension`

In this format, you must supply an `-in` argument. The `-out` argument will default to the same file name as the PDF, but as a PNG image. The `-ext` command allows the user to change this default behaviour. An `-ext` argument will be ignored if the `-out` file name includes an extension.

## Supported image types
This program supports conversion to multiple non-sequence 
image types.
This includes, but is not limited to, `.jpg`, `.png`, `.
bmp`, `.ico`, and `.webp`.

For a full list of supported file types and extensions, 
please consult the [pillow documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).