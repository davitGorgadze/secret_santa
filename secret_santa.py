import argparse
import os.path

from email_sender import EmailSender
from file_reader import FileReader, Santa
from pair_generator import PairGenerator
from password_protected_list_saver import SantaRecipientListSaver


def print_separator_lines():
    print("============================================")
    print("\n\n\n")


def main(file_name, text_template_path, debug=False, password="123456"):
    print(f"Passed filename is: {file_name}")
    print(f"Passed template file path is: {text_template_path}")
    print(f"Will print pairs {debug}")
    print(f"Password is {password}")

    # file_reader
    file_reader = FileReader(file_path=file_name)
    santas = file_reader.read_txt()
    print_separator_lines()

    # pair_generator
    pair_generator = PairGenerator(santas=santas, debug=debug)
    pairs = pair_generator.generate_pairs()
    invalid_pairs = [pair for pair in pairs if pair.sender == pair.receiver]

    if invalid_pairs:
        print(f"Invalid pairs found: {invalid_pairs}")
    else:
        print("No invalid pairs. All senders and receivers are different.")

        print_separator_lines()

        # email_sender

        email_sender = EmailSender(pairs, template_file_path=text_template_path)
        email_sender.send_all_emails()
        print_separator_lines()

        # protected txt saver
        saver = SantaRecipientListSaver(pairs, output_file="SecretSantaSecretList.zip", password=password)
        saver.save_to_password_protected_zip()


if __name__ == "__main__":
    # Command-line argument parsing
    parser = argparse.ArgumentParser(
        prog='Secret Santa',
        description='This program reads a specifically formatted txt file, pairs Santas, and sends them emails.'
    )

    parser.add_argument("--file", type=str, required=False, help="Path to the Santa list file")
    parser.add_argument("--text_template_path", type=str, required=False, help="Path to the email template")
    parser.add_argument("--debug", action="store_true", help="Print debug information")
    parser.add_argument("--password", type=str, default="123456", help="Password for the zip file")

    args = parser.parse_args()

    if args.file and args.text_template_path:
        # Command-line arguments provided
        file_name = args.file
        text_template_path = args.text_template_path
        debug = args.debug
        password = args.password

        print(f"Using command-line arguments")
        main(file_name=file_name, text_template_path=text_template_path, debug=debug, password=password)
    else:
        file_name = "data/secret_santa_all.txt"  # Path to default file
        text_template_path = "data/email_template.txt"  # Path to default template file
        debug = True
        password = "123456"

        main(file_name=file_name, text_template_path=text_template_path, debug=debug, password=password)
