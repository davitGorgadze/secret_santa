import dataclasses
import random
from typing import Set

from file_reader import Santa
from dataclasses import dataclass


@dataclass(frozen=True)
class SantaRecipientPair:
    sender: Santa
    receiver: Santa


class PairGenerator:

    def __init__(self, santas: Set[Santa], debug: bool = False):
        """
        :param santas:  Set of Santa Objects
        :param debug: if debug is True, this object will print all santa pairs
        """
        self.santas: Set[Santa] = santas
        self.debug = debug

    def generate_pairs(self):
        pairs = set()
        remaining_santas = self.santas.copy()
        remaining_recipients = list(self.santas.copy())

        while remaining_santas:
            current_santa = remaining_santas.pop()

            # Filter out current_santa from the remaining recipients
            valid_recipients = [r for r in remaining_recipients if r != current_santa]

            if not valid_recipients:
                # If no valid recipient is available, restart pairing
                print("Restarting pairing process due to impossible assignment.")
                return self.generate_pairs()

            recipient = random.choice(valid_recipients)
            remaining_recipients.remove(recipient)

            pairs.add(SantaRecipientPair(sender=current_santa, receiver=recipient))

        print("Finished Generating Pairs.")

        if self.debug:
            print(f"All Pairs are: {pairs}")

        return pairs
