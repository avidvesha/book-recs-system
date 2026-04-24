# src/preprocess/merge_book_tags.py
import pandas as pd
  
def clean_data(left_path, right_path, output_path):
    bt = pd.read_csv(left_path, index_col=0).reset_index().rename(columns={'index': 'goodreads_book_id'})
    t = pd.read_csv(right_path, index_col=0).reset_index().rename(columns={'index': 'tag_id'})
    
    # --- Paste your specific Colab logic here ---
    
    df = bt.merge(t, how='left', on='tag_id', suffixes=('', '_y'))
    
    df = df[df['tag_name'] != ""]
    df = df[df['tag_name'].notna()]
    
    df = df.drop_duplicates(subset=['goodreads_book_id', 'tag_id'], keep='first')

    # df = df.groupby('goodreads_book_id').apply(lambda x: x.nlargest(30, 'count')).reset_index(drop=True)
    df = df.groupby('goodreads_book_id')[['count', 'tag_id', 'tag_name']].apply(lambda x: x.nlargest(30, 'count')).reset_index(drop=False)

    df['tag_name'] = df['tag_name'].str.replace(r"[\[\]']", "", regex=True)
    df['tag_name'] = df['tag_name'].str.strip()
    
    book_tags_soup = df.groupby('goodreads_book_id')['tag_name'].apply(lambda x: ', '.join(x)).reset_index()

    book_tags_soup['tag_length'] = book_tags_soup['tag_name'].apply(len)

    # --------------------------------------------
    
    book_tags_soup.to_csv(output_path, index=False)
    print(f"Successfully cleaned: {output_path}")

if __name__ == "__main__":
    # You can hardcode paths or use sys.argv to make it dynamic for DVC
    clean_data("data/raw/book_tags.csv", "data/interim/cleaned_tags.csv", "data/interim/cleaned_book_tags.csv")