from dataclasses import dataclass


@dataclass(frozen=True)
class Santa:
    email: str
    name: str


class FileReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def __finished_reading(self, result):
        print(f"Finished reading the file: {self.file_path}")
        print(f"Number of Santas is {len(result)}.")
        print(f"All the santas {result}")

    def read_txt(self):
        if not self.file_path.endswith(".txt"):
            raise ValueError("Incorrect document was passed, check that file ends with .txt")

        result = set()

        # Open file using utf-8-sig to handle BOM
        with open(self.file_path, encoding="utf-8-sig") as file:
            for line in file:
                # Debug the line being read
                print(f"Reading line: {line.strip()}")

                email = line.split(",")[-1].strip()
                without_number = "".join(line.split(".")[1:])
                info = without_number.split(",")
                name = info[0].strip()

                new_santa = Santa(email=email, name=name)
                result.add(new_santa)

        self.__finished_reading(result)
        return result


if __name__ == "__main__":
    FileReader("data/Secret Santa.txt").read_txt()
