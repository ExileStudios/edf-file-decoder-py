import os
from eolib.encrypt.encryption_utils import deinterleave, swap_multiples

class DataFiles:
    """Enumeration for different types of EDF files."""
    CURSE_FILTER = 1
    CHECKSUM = 2
    CREDITS = 3
    OTHER = 4

class EDFLoaderService:
    """
    Service for loading and decoding EDF files.

    Methods:
        load_file(file_name, file_type): Loads and decodes the specified EDF file based on its type.
        save_file(file_name, data): Saves the decoded data to a text file.
    """
    def load_file(self, file_name, file_type):
        """
        Loads and decodes an EDF file based on its type.

        Args:
            file_name (str): The path to the EDF file.
            file_type (int): The type of EDF file.

        Returns:
            str: The decoded content of the EDF file.
        """
        if file_type in {DataFiles.CHECKSUM, DataFiles.CREDITS}:
            return self._load_unencoded_file(file_name)
        else:
            return self._load_and_decode(file_name, file_type)

    @staticmethod
    def save_file(file_name, data):
        """
        Saves the decoded data to a text file.

        Args:
            file_name (str): The path to the output text file.
            data (str): The decoded data to be saved.
        """
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(data)

    def _load_and_decode(self, file_name, file_type):
        """
        Loads and decodes an encoded EDF file.

        Args:
            file_name (str): The path to the EDF file.
            file_type (int): The type of EDF file.

        Returns:
            str: The decoded content of the EDF file.
        """
        with open(file_name, 'r', encoding='latin-1') as f:
            lines = f.readlines()

        decoded_lines = [self._decode_dat_string(line.strip(), file_type) for line in lines]
        return '\n'.join(decoded_lines)

    @staticmethod
    def _load_unencoded_file(file_name):
        """
        Loads an unencoded EDF file.

        Args:
            file_name (str): The path to the EDF file.

        Returns:
            str: The content of the EDF file.
        """
        with open(file_name, 'r', encoding='latin-1') as f:
            return f.read()

    @staticmethod
    def _decode_dat_string(content, file_type):
        """
        Decodes a string from an EDF file.

        Args:
            content (str): The encoded string.
            file_type (int): The type of EDF file.

        Returns:
            str: The decoded string.
        """
        byte_data = bytearray(content.encode('latin-1'))
        deinterleave(byte_data)
        if file_type != DataFiles.CURSE_FILTER:
            swap_multiples(byte_data, 7)
        return byte_data.decode('latin-1')

def parse_all_edf_files():
    """
    Parses all EDF files in the current directory, decodes them, and saves the decoded content to text files.
    """
    current_dir = os.getcwd()
    data_files = [f for f in os.listdir(current_dir) if f.endswith('.edf')]

    edf_loader = EDFLoaderService()

    # Mapping EDF file numbers to their types
    file_type_map = {
        1: DataFiles.CHECKSUM,
        2: DataFiles.CREDITS,
        3: DataFiles.CURSE_FILTER
    }

    for data_file in data_files:
        file_path = os.path.join(current_dir, data_file)
        file_number = int(data_file[3:6])  # Extract the number from the file name
        file_type = file_type_map.get(file_number, DataFiles.OTHER)

        edf_data = edf_loader.load_file(file_path, file_type)
        output_file = data_file.replace('.edf', '.txt')
        edf_loader.save_file(output_file, edf_data)
        print(f"Decoded content of {data_file} saved to {output_file}.")

if __name__ == "__main__":
    parse_all_edf_files()
