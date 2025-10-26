from unittest.mock import patch

from pytest import raises

from src.pdf_converter_cli import get_write_path, get_option_key_value_pairs, pdf_converter_cli

class TestPDFConverterCli:
    class TestCliCommand:
        @patch("src.pdf_converter_cli.cli_help")
        @patch("src.pdf_converter_cli.cli_convert_to_image")
        def test_should_call_the_help_command(self, mock_cli_convert_to_image, mock_cli_help):
            pdf_converter_cli("python_exe_command help".split(" "))
            assert mock_cli_help.call_count == 1
            assert mock_cli_convert_to_image.call_count == 0

        @patch("src.pdf_converter_cli.cli_help")
        @patch("src.pdf_converter_cli.cli_convert_to_image")
        def test_should_call_the_convert_command(self, mock_cli_convert_to_image, mock_cli_help):
            pdf_converter_cli("python_exe_command convert arg1 arg2 arg3".split(" "))
            assert mock_cli_help.call_count == 0
            assert mock_cli_convert_to_image.call_count == 1

        def test_should_throw_an_exception_if_unrecognised_command_provided(self):
            with raises(ValueError):
                pdf_converter_cli("python_exe_command unrecognised_command".split(" "))

    class TestGetOptionKeyValuePairs:
        def test_should_pick_up_options_from_arguments(self):
            args = ["python_exe_command", "command", "-in", "pdf_path.pdf", "-out", "png_path.png", "-ext", ".extension"]
            result = get_option_key_value_pairs(args)

            assert result == {
                "-in": "pdf_path.pdf",
                "-out": "png_path.png",
                "-ext": ".extension",
            }

        def test_should_infer_input_file_from_arguments(self):
            args = ["python_exe_command", "command", "pdf_path.pdf"]
            result = get_option_key_value_pairs(args)

            assert result == {
                "-in": "pdf_path.pdf",
                "-out": None,
                "-ext": None
            }

        def test_should_infer_input_file_and_output_file_from_arguments(self):
            args = ["python_exe_command", "command", "pdf_path.pdf", "png_path.png"]
            result = get_option_key_value_pairs(args)

            assert result == {
                "-in": "pdf_path.pdf",
                "-out": "png_path.png",
                "-ext": None
            }

        def test_should_not_infer_values_if_option_provided(self):
            args = ["python_exe_command", "command", "-in", "pdf_path.pdf"]
            result = get_option_key_value_pairs(args)

            assert result == {
                "-in": "pdf_path.pdf",
                "-out": None,
                "-ext": None,
            }

            args = ["python_exe_command", "command", "-out", "png_path.png"]
            result = get_option_key_value_pairs(args)

            assert result == {
                "-in": None,
                "-out": "png_path.png",
                "-ext": None,
            }

            args = ["python_exe_command", "command", "-ext", ".extension"]
            result = get_option_key_value_pairs(args)

            assert result == {
                "-in": None,
                "-out": None,
                "-ext": ".extension",
            }

    class TestGetWritePath:
        def test_should_append_png_extension_if_no_extension_and_to_path_provided(self):
            result = get_write_path("from_path.pdf", None, None)
            assert result == "from_path.png"

        def test_should_append_png_extension_if_filename_has_no_extension_and_no_extension_provided(self):
            result = get_write_path("from_path.pdf", "to_path", None)
            assert result == "to_path.png"

        def test_should_append_given_extension_if_no_to_path_provided(self):
            result = get_write_path("from_path.pdf", None, ".jpg")
            assert result == "from_path.jpg"

        def test_should_ignore_provided_extension_if_filename_already_has_extension(self):
            result = get_write_path("from_path.pdf", "to_path.jpg", ".webp")
            assert result == "to_path.jpg"

        def test_should_append_given_extension_to_given_filepath_if_path_has_no_extension(self):
            result = get_write_path("from_path.pdf", "to_path", ".webp")
            assert result == "to_path.webp"

        def test_should_raise_exception_if_from_path_is_not_provided(self):
            with raises(ValueError):
                get_write_path(None, "doesnt-matter", "doesnt-matter")

        def test_should_append_period_if_is_missing_from_extension(self):
            result = get_write_path("from_path.pdf", "to_path", "webp")
            assert result == "to_path.webp"

        def test_should_append_period_if_is_missing_from_extension_and_no_to_path(self):
            result = get_write_path("from_path.pdf", None, "webp")
            assert result == "from_path.webp"
