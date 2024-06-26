# EDF File Decoder

This script parses and decodes all `.edf` files in the current directory and saves the decoded content to `.txt` files.

## Features

- Decodes various types of EDF files including Curse Filter, Checksum, and Credits.
- Handles encoded and unencoded EDF files.
- Uses interleave and deinterleave algorithms for decoding.

## Requirements

- Python 3.x
- `eolib` package

## Installation

1. Clone the repository or download the script.
2. Install the required package using pip:

```bash
pip install -r requirements.txt
```

## Usage

Place the script in the directory containing your `.edf` files and run the script:

```bash
python main.py
```

## eolib-python

This project uses the eolib-python library for data encryption and decryption. You can find the library on GitHub: [eolib-python](https://github.com/Cirras/eolib-python)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
