# Word Tokenizer

A lightweight **word-level tokenizer implemented in pure Python**.

This project is being developed as part of a from-scratch tokenizer/LLM pipeline. It currently focuses on preparing text data from PDF documents and converting text into word-level tokens while preserving whitespace and punctuation as tokenizer-relevant information.

## Project Goals

The main goals of this project are:

- Build a tokenizer from scratch instead of relying on an existing tokenizer library.
- Collect text from a directory containing PDF documents.
- Prepare a clean corpus for tokenizer training.
- Split text into words, whitespace, and punctuation.
- Build a vocabulary from the resulting tokens.
- Convert tokens to integer IDs.
- Provide a foundation for later tokenizer experiments such as BPE and byte-level BPE.

## Project Structure

```text
word-tokenizer/
│
├── datasets/
│   └── *.pdf                 # Source PDF documents
│
├── data.txt                  # Extracted text corpus
│
├── loader.py                 # PDF loading and text extraction
├── pipeline.py               # Data/tokenization pipeline entry point
├── Tokenizer.py              # Word tokenizer implementation
│
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

> The exact contents of individual Python modules may evolve as the tokenizer is developed.

## Pipeline

The current data flow is:

```text
PDF Documents
      │
      ▼
   loader.py
      │
      │ PyMuPDF
      ▼
   data.txt
      │
      ▼
 Tokenizer.py
      │
      ▼
 Word Tokens
      │
      ▼
 Vocabulary
      │
      ▼
 Token IDs
```

## 1. Dataset Preparation

Place your PDF documents inside the `datasets/` directory.

Example:

```text
datasets/
├── book1.pdf
├── book2.pdf
├── paper.pdf
└── document.pdf
```

The loader scans the directory recursively for PDF files and extracts their text.

## 2. PDF Text Extraction

`loader.py` uses **PyMuPDF** to read PDF files.

The basic process is:

```python
import pymupdf
from pathlib import Path
```

The loader:

1. Opens the output corpus file.
2. Converts the dataset path to a `Path`.
3. Searches for PDF files recursively.
4. Opens each PDF.
5. Iterates through its pages.
6. Extracts page text.
7. Writes the extracted text to `data.txt`.
8. Closes the PDF.

Conceptually:

```text
datasets/
    ├── book1.pdf
    ├── book2.pdf
    └── book3.pdf

        │
        ▼

     loader.py

        │
        ▼

     data.txt
```

## 3. Word Tokenization

The tokenizer operates on the extracted text.

A useful starting regular expression for this project is:

```python
r"\w+|[^\w\s]|\s+"
```

This separates:

- Words
- Punctuation
- Whitespace

For example:

```text
Hello,  world!
```

can become:

```python
[
    "Hello",
    ",",
    "  ",
    "world",
    "!"
]
```

Keeping whitespace is useful when experimenting with language-model tokenization because whitespace contains information about the original text structure.

## 4. Vocabulary

After tokenization, the unique tokens can be collected into a vocabulary.

For example:

```python
{
    "Hello": 0,
    ",": 1,
    " ": 2,
    "world": 3,
    "!": 4
}
```

The mapping allows text tokens to be converted into integer IDs.

Example:

```text
["Hello", ",", "world", "!"]
```

becomes:

```text
[0, 1, 3, 4]
```

The exact vocabulary-building implementation is defined by `Tokenizer.py`.

## 5. Special Tokens

As the tokenizer develops, special tokens can be introduced for language-model training.

Typical examples include:

```text
<UNK>   Unknown token
<PAD>   Padding
<BOS>   Beginning of sequence
<EOS>   End of sequence
```

These should have reserved vocabulary IDs so that normal text tokens cannot collide with them.

Example:

```python
special_tokens = {
    "<PAD>": 0,
    "<UNK>": 1,
    "<BOS>": 2,
    "<EOS>": 3,
}
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd word-tokenizer
```

### 2. Create a virtual environment

Using Python's built-in virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project currently uses **PyMuPDF** for PDF text extraction.

## Usage

Place PDF files inside:

```text
datasets/
```

Then run the pipeline:

```bash
python pipeline.py
```

The pipeline can generate/update:

```text
data.txt
```

with the extracted corpus.

Tokenizer experiments can then be run through:

```bash
python Tokenizer.py
```

depending on the current implementation.

## Example

Input:

```text
Hello, world!
This is a tokenizer.
```

Possible token output:

```python
[
    "Hello",
    ",",
    " ",
    "world",
    "!",
    "
",
    "This",
    " ",
    "is",
    " ",
    "a",
    " ",
    "tokenizer",
    "."
]
```

These tokens can then be mapped to vocabulary IDs.

## Design Philosophy

This project intentionally starts with a simple tokenizer implementation rather than immediately using a production tokenizer library.

The development path is:

```text
Word Tokenizer
      │
      ▼
Character Tokenizer
      │
      ▼
BPE Tokenizer
      │
      ▼
Byte-Level BPE
      │
      ▼
Production-Grade Tokenizer
```

This makes it possible to understand the underlying mechanics of tokenization instead of treating the tokenizer as a black box.

## Limitations

The current word-tokenizer approach has several limitations:

- Regex-based tokenization is language dependent.
- `\w` does not represent every linguistic concept of a "word".
- PDF text extraction can produce broken reading order or formatting artifacts.
- Scanned/image-only PDFs require OCR.
- Very large corpora require more careful memory and I/O handling.
- Word-level vocabularies can become extremely large.
- Word-level tokenization has poor handling of unseen words compared with subword tokenization.

These limitations are expected because this project is a learning and research-oriented tokenizer implementation.

## Future Development

Planned improvements include:

### Tokenizer

- [ ] Robust Unicode handling
- [ ] Improved punctuation handling
- [ ] Contraction handling
- [ ] Number handling
- [ ] Special-token support
- [ ] Vocabulary serialization
- [ ] Token-to-ID encoding
- [ ] ID-to-token decoding
- [ ] Save/load tokenizer configuration

### Data Pipeline

- [ ] Better PDF cleaning
- [ ] Duplicate-document detection
- [ ] Unicode normalization
- [ ] Whitespace normalization options
- [ ] OCR support for scanned PDFs
- [ ] Dataset statistics
- [ ] Streaming large datasets

### Subword Tokenization

- [ ] Implement BPE from scratch
- [ ] Efficient pair-frequency counting
- [ ] Merge-rule serialization
- [ ] Fast encoding
- [ ] Byte-level BPE
- [ ] Benchmark against existing tokenizers

## Dependencies

The project currently relies primarily on:

```text
PyMuPDF
```

Python's standard-library modules such as `re` and `pathlib` do not need to be installed separately.

## Development

Recommended Python version:

```text
Python 3.10+
```

Check your Python version:

```bash
python --version
```

## License

Add the project's license here when one is selected.

For example:

```text
MIT License
```

## Author

Developed as a from scratch tokenizer project for studying the internal components of modern NLP and LLM systems.
 