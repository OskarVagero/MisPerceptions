import pandas as pd
import time
from transformers import pipeline
#import emoji
import sys

LANG = sys.argv[1]

def analyze_emoji_sentiment(text):
    # Extract emojis from text
    emojis = [char for char in text if char in emoji.UNICODE_EMOJI['en']]
    
    # Initialize sentiment counts
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    
    # Count sentiment based on emojis
    for em in emojis:
        sentiment = emoji_sentiment_mapping.get(em, "neutral")
        sentiment_counts[sentiment] += 1
    
    # Determine overall sentiment based on counts
    if sentiment_counts["positive"] > sentiment_counts["negative"]:
        return "positive"
    elif sentiment_counts["negative"] > sentiment_counts["positive"]:
        return "negative"
    else:
        return "neutral"


def analyze_sentiment_batch(df, column_name='translated_text', batch_size=20):
    """
    Analyze sentiment of texts in batches and update the DataFrame with sentiment scores and labels.
    
    Args:
    - df: DataFrame containing the texts to analyze in `column_name`.
    - column_name: The name of the column with the text to analyze.
    - batch_size: The size of each batch of texts to process at a time.
    
    Returns:
    - The DataFrame with added 'sentiment_score' and 'sentiment_label' columns.
    """
    
    # Prepare columns for sentiment scores and labels
    print('probe')
    df['sentiment_score'] = 0.0
    df['sentiment_label'] = ''
    
    # Process texts in batches
    total_batches = len(df) // batch_size + (1 if len(df) % batch_size else 0)
    for i in range(0, len(df), batch_size):
        batch_texts = df[column_name].iloc[i:i+batch_size].tolist()
        results = sentiment_pipeline(batch_texts, truncation=True)
        
        # Update DataFrame with results
        for j, result in enumerate(results):
            df.at[i+j, 'sentiment_score'] = result['score']
            df.at[i+j, 'sentiment_label'] = result['label']
        
        # Print progress
        print(f"Processed batch {i//batch_size + 1}/{total_batches}")
    
    return df

sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

#df_text = pd.read_csv(f'{LANG}/full_text_translated')
#head_sent = analyze_sentiment_batch(df_text, column_name='translated_sentence')
#head_sent.to_csv(f'{LANG}text_sentiment.csv')

print('headlines')
df_headlines = pd.read_csv(f'{LANG}/df_headlines_tranlated.csv')
head_sent = analyze_sentiment_batch(df_headlines)
head_sent.to_csv(f'{LANG}/headline_sentiment.csv')

print('tweets')
df_tweets = pd.read_csv(f'{LANG}/df_tweets_tranlated.csv')
tweet_sent = analyze_sentiment_batch(df_tweets)
tweet_sent.to_csv(f'{LANG}/twitter_sentiment.csv')
