import pandas as pd
import time
from deep_translator import GoogleTranslator
from transformers import pipeline
import sys

LANG = sys.argv[1]
language_dict = {
    'AT': {'country': 'austria', 'langcode': 'de', 'code': 'de'},
    'NO': {'country': 'norway', 'langcode': 'no', 'code': 'no'},
    'DE': {'country': 'germany', 'langcode': 'de', 'code': 'de'},
    'DK': {'country': 'denmark', 'langcode': 'da', 'code': 'dk'},
    }

# Initialize the translator and sentiment analysis pipeline
translator = GoogleTranslator(source=language_dict[LANG]['langcode'], target='en')
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def translate_text(df, text_column):
    """
    Translate texts in a DataFrame and return a new DataFrame with original and translated texts.
    
    Args:
    - df: DataFrame containing the texts to translate.
    - text_column: The name of the column containing the texts.
    
    Returns:
    - A new DataFrame with original texts, translated texts.
    """
    # Initialize an empty DataFrame
    translated_df = pd.DataFrame(columns=['original_text', 'translated_text'])
    
    # Translate each text and store in the new DataFrame
    tt = 0
    for text in df[text_column]:
        translated_text = translator.translate(text)
        time.sleep(0.1)
        print(tt, df[text_column].size) ; tt += 1
        translated_df = pd.concat([translated_df, pd.DataFrame({'original_text': text, 'translated_text': translated_text}, index=[0])], ignore_index=True)
    
    return translated_df


print('headlines')
df_headlines = pd.read_csv(f'{LANG}/{LANG.lower()}_headlines_filtered.csv')
#df_headlines = pd.read_excel(f"Headlines/{language_dict[LANG]['code']}_df.xlsx")
df_headlines_translated = translate_text(df_headlines, 'title')
df_headlines_merged = pd.merge(df_headlines, df_headlines_translated, left_on='title', right_on='original_text')
df_headlines_merged.to_csv(f'{LANG}/df_headlines_tranlated.csv')

print('tweets')
#df_headlines = pd.read_csv(f"Twitter/{language_dict[LANG]['country']}_geolocated_2010_2022_anonymous.csv")
df_tweets = pd.read_csv(f'{LANG}/{LANG.lower()}_tweets_filtered.csv')
df_tweets_translated = translate_text(df_tweets, 'text')
df_tweets_merged = pd.merge(df_tweets, df_tweets_translated, left_on='text', right_on='original_text')
df_tweets_merged.to_csv(f'{LANG}/df_tweets_tranlated.csv')

