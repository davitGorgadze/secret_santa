from typing import Set

import pyminizip
import pyzipper

from file_reader import Santa
from pair_generator import SantaRecipientPair


class SantaRecipientListSaver:

    def __init__(self, pairs: Set[SantaRecipientPair], output_file: str, password: str, compression_level: int = 5):
        """
        Initialize the SantaRecipientListSaver with pairs, output file path, password, and compression level.

        :param pairs: Set of SantaRecipientPair objects.
        :param output_file: Path to save the password-protected zip file.
        :param password: Password for the zip file.
        :param compression_level: Compression level (0-9) for the ZIP file. Default is 5.
        """
        self.pairs = pairs
        self.output_file = output_file
        self.password = password
        self.compression_level = compression_level

    def _create_recipient_list_file(self, file_name: str):
        """
        Create a text file containing the Secret Santa recipient list.

        :param file_name: Name of the file to save the recipient list.
        """
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write("სანტას სია:\n\n\n\n")
            for pair in self.pairs:
                file.write(
                    f"სანტა: {pair.sender.name} ({pair.sender.email}) -> ადრესატი: {pair.receiver.name} ({pair.receiver.email})\n")

    def save_to_password_protected_zip(self):
        """
        Save the recipient list to a password-protected zip file.
        """
        temp_file = "recipient_list.txt"

        # Create the recipient list as a plain text file
        self._create_recipient_list_file(temp_file)

        pyminizip.compress(
            temp_file,
            None,
            self.output_file,
            self.password,
            self.compression_level
        )

        print(f"Recipient list saved to {self.output_file} with password protection.")


if __name__ == "__main__":
    pairs = {
        SantaRecipientPair(
            sender=Santa(email="alice@example.com", name="Alice"),
            receiver=Santa(email="bob@example.com", name="Bob")
        ),
        SantaRecipientPair(
            sender=Santa(email="charlie@example.com", name="Charlie"),
            receiver=Santa(email="dana@example.com", name="Dana")
        )
    }

    output_file = "secret_santa.zip"
    password = "noneshallpass"

    saver = SantaRecipientListSaver(pairs, output_file, password)
    saver.save_to_password_protected_zip()
