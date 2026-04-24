# src/preprocess/clean_books.py
import pandas as pd
import re

def preprocess_authors(author_str):
    if not isinstance(author_str, str) or not author_str.strip():
        return ""

    authors_list = author_str.split(',')

    processed_authors = []
    for author in authors_list:
        name = author.lower().strip()
        
        name = re.sub(r'[^a-z0-9\s]', '', name)
        
        name = name.replace(' ', '_')
        
        processed_authors.append(f"author_{name}")

    return " ".join(processed_authors)
  
def preprocess_decade(year):
    if pd.isna(year) or year < 0:
        return "decade_unknown"
    
    decade = int((year // 10) * 10)
    
    return f"decade_{decade}s"
  
def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # --- Paste your specific Colab logic here ---
    
    lang_map = {
    'en-US': 'eng',
    'en-GB': 'eng',
    'en-CA': 'eng',
    'en': 'eng'
    }
    df['language_code'] = df['language_code'].replace(lang_map)
    
    # --------------------------------------------
    
    df = df[df['language_code'] == 'eng']
    df = df[['id', 'book_id', 'title', 'authors', 'original_publication_year']]

    # --------------------------------------------
    
    df['authors'] = df['authors'].apply(preprocess_authors)
    df['original_publication_year'] = df['original_publication_year'].apply(preprocess_decade)
    df.rename(columns={'original_publication_year': 'decade_year'}, inplace=True)

    # --------------------------------------------
    
    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned: {output_path}")

if __name__ == "__main__":
    # You can hardcode paths or use sys.argv to make it dynamic for DVC
    clean_data("data/raw/books.csv", "data/interim/cleaned_books.csv")