from os import path, mkdir
from shutil import rmtree

from src.pdf_converter import PDFConverter
from pytest import raises, fixture, mark

class TestPDFConverter:
    class TestReadFile:
        def test_opens_demo_file_successfully(self):
            file = PDFConverter("./res/demo_file.pdf")
            assert file.read_data is not None and len(file.read_data) > 0

        def test_throws_exception_when_non_pdf_file_supplied(self):
            with raises(IOError):
                PDFConverter("./res/demo_file.png")

        def test_throws_exception_when_file_does_not_exist(self):
            with raises(FileNotFoundError):
                PDFConverter("./res/made_up_file.pdf")

    class TestWriteFile:
        @fixture(autouse=True)
        def teardown_and_cleanup(self):
            if not path.isdir("./res/tmp"):
                mkdir("./res/tmp/")
            yield
            rmtree("./res/tmp/")

        def test_writes_pdf_file_successfully(self):
            PDFConverter("./res/demo_file.pdf").save_as_pdf("./res/tmp/demo_file.pdf")
            assert path.exists("./res/tmp/demo_file.pdf")

        image_file_test_data = [
            "./res/tmp/demo_file.png",
            "./res/tmp/demo_file.jpg",
            "./res/tmp/demo_file.jpeg",
            "./res/tmp/demo_file.bmp",
            "./res/tmp/demo_file.gif",
            "./res/tmp/demo_file.ico",
            "./res/tmp/demo_file.webp",
        ]

        @mark.parametrize("write_file", image_file_test_data)
        def test_writes_image_file_successfully(self, write_file):
            PDFConverter("./res/demo_file.pdf").save_as_image(write_file)
            assert path.exists(write_file)

        def test_writes_jpg_file_successfully(self):
            PDFConverter("./res/demo_file.pdf").save_as_image("./res/tmp/demo_file.jpg")
            assert path.exists("./res/tmp/demo_file.jpg")

        def test_throws_exception_when_unrecognised_file_type_supplied(self):
            with raises(ValueError):
                PDFConverter("./res/demo_file.pdf").save_as_image("./res/tmp/demo_file.made_up_filetype")
            assert not path.exists("./res/tmp/demo_file.made_up_filetype")

        def test_throws_exception_when_write_path_does_not_exist(self):
            with raises(IOError):
                PDFConverter("./res/demo_file.pdf").save_as_image("./res/tmp/dir/does/not/exist/demo_file.pdf")