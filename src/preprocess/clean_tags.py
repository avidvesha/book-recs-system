# src/preprocess/clean_tags.py
import pandas as pd
import re
from deep_translator import GoogleTranslator
import unicodedata
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')

def needs_translation(text):
    # Returns True if the text contains Arabic characters or other non-Latin scripts
    return bool(re.search(r'[^\x00-\x7F]+', str(text)))
  
def super_clean_tags(text):
    if not isinstance(text, str) or not text.strip():
        return []

    text = unicodedata.normalize('NFKC', text)
    text = text.encode("ascii", "ignore").decode()
    text = text.lower()

    raw_tags = text.split(',')

    lemmatizer = WordNetLemmatizer()
    tag_stop_words = {
        'toread', 'currentlyreading', 'read', 'owned', 'book', 'shelf',
        'favorite', 'favourite', 'alltimefavorite', 'mustread', 'kindle',
        'ebook', 'library', 'default', 'own', 'readin', 'المفضلة'
    }

    junk_patterns = {'error', 'server', 'try_again', 'thats_all', 'know', 'http', 'book', 'read'}

    final_processed_tags = []

    for tag in raw_tags:
        if any(junk in tag for junk in junk_patterns) or len(tag) > 50:
            continue

        components = re.split(r'[-_\s]+', tag)
        processed_comp = []

        for comp in components:
            comp = re.sub(r'[^a-z\u0600-\u06FF]', '', comp)
            comp = lemmatizer.lemmatize(comp)

            if comp not in tag_stop_words and len(comp) > 2:
                processed_comp.append(comp)

        if processed_comp:
            final_tag = "_".join(processed_comp)
            final_processed_tags.append(final_tag)

    return final_processed_tags

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # --- Paste your specific Colab logic here ---
    
    df_to_translate = df[df['tag_name'].apply(needs_translation)]['tag_name'].unique()
    
    # --------------------------------------------
    
    translation_dict = {}
    for original in df_to_translate:
      try:
          # We translate only the unique string once
          translated = GoogleTranslator(source='auto', target='en').translate(original)
          translation_dict[original] = translated
      except Exception as e:
          translation_dict[original] = original 
          
    df['tag_name_translated'] = df['tag_name'].map(translation_dict).fillna(df['tag_name'])
    
    # --------------------------------------------
    
    df['tag_name_cleaned'] = df['tag_name_translated'].apply(super_clean_tags)
    df = df[df['tag_name_cleaned'].apply(lambda x: len(x) > 0)]
    df.dropna(subset=['tag_name_cleaned'], inplace=True)
    df = df[df['tag_name_cleaned'] != '']

    # --------------------------------------------
    
    df = df[['tag_id', 'tag_name_cleaned']]
    df.rename(columns={'tag_name_cleaned': 'tag_name'}, inplace=True)

    # --------------------------------------------
    
    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned: {output_path}")

if __name__ == "__main__":
    # You can hardcode paths or use sys.argv to make it dynamic for DVC
    clean_data("data/raw/tags.csv", "data/interim/cleaned_tags.csv")