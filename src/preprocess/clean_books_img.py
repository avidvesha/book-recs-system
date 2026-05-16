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
        return "decade_0s"
    
    decade = int((year // 10) * 10)
    
    return f"decade_{decade}s"
  
def clean_data(left_path, right_path, output_path):
    clean = pd.read_csv(right_path)
    raw = pd.read_csv(left_path)
    
    # --- Paste your specific Colab logic here ---
    
    raw = raw[["id", "title", "authors", "original_publication_year", "image_url", "language_code"]]
    
    idx = raw[['original_publication_year', 'title']][raw['original_publication_year'].isna()].index

    years = [2008, 1996, 2003, 2003, 2009, 2003, 2010, 2009, 2013, 2010, 1859, 
             2006, 2010, 1982, 2012, 2000, 1974, 1950, 2009, 2007, 2009]

    update_series = pd.Series(years, index=idx)
    
    raw['original_publication_year'].update(update_series)
    
    lang_map = {
    'en-US': 'eng',
    'en-GB': 'eng',
    'en-CA': 'eng',
    'en': 'eng'
    }
    
    raw['language_code'] = raw['language_code'].replace(lang_map)
    
    raw = raw[raw['language_code'] == 'eng']
    
    # --------------------------------------------
    
    raw.rename(columns={
        'authors': 'raw_authors',
        'original_publication_year': 'raw_year',
        }, inplace=True)
    
    # --------------------------------------------

    df = pd.merge(clean, raw, on="id", how="inner")

    # --------------------------------------------
    
    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned: {output_path}")

if __name__ == "__main__":
    # You can hardcode paths or use sys.argv to make it dynamic for DVC
    clean_data("data/raw/books.csv", "data/interim/cleaned_books.csv", "data/processed/cleaned_books_with_img.csv")