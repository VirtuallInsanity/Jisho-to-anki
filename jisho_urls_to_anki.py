import configparser
import requests
from bs4 import BeautifulSoup
import genanki

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

# path to url file
url_file_path = config['Files']['url_file']
num_meanings = config['Jisho'].getint('num_meanings')


# Jisho extractor
def extract_word_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract words and furigana
    concept_light = soup.select_one('.concept_light')
    if not concept_light:
        return None, None

    concept_light_repres = soup.select_one('.concept_light-representation')
    if not concept_light_repres:
        return None, None
    kanji_elements = concept_light.select('.text')[0].get_text(strip=True) if concept_light.select('.text') else None
    furigana_elements = concept_light.select('.furigana > .kanji')
    if not kanji_elements:
        return None, None

    # Build the ruby structure
    ruby_structure = ""
    furigana_index = 0

    for kanji in kanji_elements:
        # Ensure only kanji has furigana mapping
        if 0x4E00 <= ord(kanji) <= 0x9FAF:  # Kanji Unicode range
            try:
                furigana_element = furigana_elements[furigana_index]
            except IndexError:
                ruby_structure += kanji
                continue

            furigana_index += 1
            furigana = furigana_element.get_text(strip=True)

            # Add ruby for this kanji
            ruby_structure += f"<ruby>{kanji}<rt>{furigana}</rt></ruby>"
        else:
            # Add non-kanji characters directly
            ruby_structure += kanji

    # Extraction of types, meaning and examples only from the first .meanings-wrapper block (First word from jisho page)
    meanings_wrapper = concept_light.select_one('.meanings-wrapper')
    word_types = meanings_wrapper.select('.meaning-tags') if meanings_wrapper else []
    senses = meanings_wrapper.select('.meaning-wrapper') if meanings_wrapper else []

    entries = []
    for i, sense in enumerate(senses[:num_meanings]):
        pos = sense.select_one('.meaning-meaning').get_text(strip=True) if sense.select_one(
            '.meaning-meaning') else "N/A"

        pos = str(i + 1) + '. ' + pos

        japanese_sentence = sense.select_one('.japanese')
        english_sentence = sense.select_one('.english')

        if not japanese_sentence:
            entries.append(f"{word_types[i].get_text(strip=True)}<br>{pos}")
            continue

        ruby_sentence = ""
        for li in japanese_sentence.find_all('li', class_='clearfix'):
            # Check for furigana and kanji
            furigana = li.find('span', class_='furigana')
            kanji = li.find('span', class_='unlinked')

            if furigana and kanji:
                # Add ruby tag for kanji with furigana
                ruby_sentence += f"<ruby>{kanji.text}<rt>{furigana.text}</rt></ruby>"
            elif kanji:
                # Add plain kanji or text without furigana
                ruby_sentence += kanji.text
            else:
                # Handle punctuation or additional non-text elements
                ruby_sentence += li.get_text(strip=True)

        english_text = english_sentence.get_text(strip=True) if english_sentence else ""

        entries.append(f"{word_types[i].get_text(strip=True)}<br>{pos}<br>{ruby_sentence}<br>{english_text}")
    print(ruby_structure, '|', entries)
    print('---')
    return ruby_structure, entries


# Read links from file
with open(url_file_path, 'r') as file:
    urls = file.read().splitlines()
    print('Found URLs: ' + str(len(urls)))

# Anki card
my_model = genanki.Model(
    config['Model'].getint('model_id'),
    config['Model']['model_name'],
    fields=[
        {"name": "Front"},
        {"name": "Back"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": "{{FrontSide}}<hr id='answer'>{{Back}}",
        },
    ],
)

cnt = 1
my_deck = genanki.Deck(config['Deck'].getint('deck_id'), config['Deck']['deck_name'])
for url in urls:
    print(str(cnt))
    try:
        ruby_structure, entries = extract_word_data(url)
        if ruby_structure and entries:
            front = ruby_structure  # f"<ruby>{word}<rt>{reading}</rt></ruby>"
            back = "<br><br>".join(entries)
            note = genanki.Note(
                model=my_model,
                fields=[front, back],
            )
            my_deck.add_note(note)
        else:
            print('Skipped URL: ', url)
            print('Check the URL!')
    except Exception as e:
        print(f"Error processing {url}: {e}")
    cnt += 1

# Save deck
output_file = config['Files']['output_apkg_file']
genanki.Package(my_deck).write_to_file(output_file)
print(f"Deck saved as {output_file}")
