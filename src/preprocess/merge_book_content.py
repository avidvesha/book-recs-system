# src/preprocess/merge_book_content.py
import pandas as pd
  
def clean_data(left_path, right_path, output_path):
    b = pd.read_csv(left_path)
    ts = pd.read_csv(right_path)
    
    # --- Paste your specific Colab logic here ---
    
    df = b.merge(right=ts, how='left', left_on='book_id', right_on='goodreads_book_id')

    # --------------------------------------------
    
    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned: {output_path}")

if __name__ == "__main__":
    # You can hardcode paths or use sys.argv to make it dynamic for DVC
    clean_data("data/interim/cleaned_books.csv", "data/interim/cleaned_book_tags.csv", "data/processed/final_book_features.csv")