# Jisho-to-anki
Convert Jisho.org word pages into Anki flashcards automatically.

## Features
- Extracts kanji, readings, meanings, and example sentences
- Preserves furigana with proper ruby formatting
- Customizable number of meanings per card

## Installation
1. Install Python 3.9
2. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Create a text file with Jisho.org URLs (one per line)
2. Update `config.ini` with your preferences
3. Run the script: `python jisho_urls_to_anki.py`
4. Import the generated `.apkg` file into Anki

## Configuration
Edit `config.ini` to:
- Set input/output file paths
- Control how many meanings are included
- Customize deck and card appearance

## Example URLs File
https://jisho.org/search/%E6%81%A5%E3%81%9A%E3%81%8B%E3%81%97%E3%81%84
https://jisho.org/search/%E4%BB%98%E3%81%91%E3%82%8B

# How to get Jisho urls
You can use this extension: https://chromewebstore.google.com/detail/odclbaijmmabcgcdaipkpkcmfkfifgea?utm_source=item-share-cb <br/>
Or you can use any other method that suits you, but the format of .txt should be the same. <br/>

**Important:** Words in the links should be written with __kanji__ <br/>
**For example:** The link sould be pointing to the word written this way **付ける** and not this way **つける**
