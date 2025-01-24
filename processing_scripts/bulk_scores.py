import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.patches import Rectangle
import numpy as np

def load_data(country, ID):
   file_path = f'{country}/{ID}_sentiment.csv'
   return pd.read_csv(file_path)

country_names = {'DE': 'Germany', 'DK': 'Denmark', 'NO': 'Norway', 'AT': 'Austria'}

focus_topics = {
   'a_bird_bat': 'bird bat',
   'c_visual': 'visual',
   'f_participation': 'participation', 
   'p_long_planning': 'long planning'
}

def get_color_gradient(sentiment):
   if pd.isna(sentiment):
       return '#CCCCCC'
       
   if sentiment >= 0:
       pal = sns.color_palette("Reds", n_colors=100)
       idx = int(min(abs(sentiment), 1) * 60)
       return f'#{int(pal[idx][0]*255):02x}{int(pal[idx][1]*255):02x}{int(pal[idx][2]*255):02x}'
   else:
       pal = sns.color_palette("Blues", n_colors=100) 
       idx = int(min(abs(sentiment), 1) * 60)
       return f'#{int(pal[idx][0]*255):02x}{int(pal[idx][1]*255):02x}{int(pal[idx][2]*255):02x}'

def plot_specific_topics(dat, ax, title, confidence_threshold=0.8):
   dat['numerical_sentiment'] = dat['sentiment_label'].map({'LABEL_0': -1, 'LABEL_1': 0, 'LABEL_2': 1})
   dat = dat[dat['topic'].isin(focus_topics.keys())]

   topic_sentiment_avg = dat.groupby('topic')['numerical_sentiment'].mean().reset_index()
   topic_sentiment_sem = dat.groupby('topic')['numerical_sentiment'].sem().reset_index()

   high_confidence_data = dat[dat['sentiment_score'] > confidence_threshold]
   topic_high_conf_avg = high_confidence_data.groupby('topic')['numerical_sentiment'].mean().reset_index()
   topic_high_conf_sem = high_confidence_data.groupby('topic')['numerical_sentiment'].sem().reset_index()

   topic_sentiment_avg = topic_sentiment_avg.rename(columns={'numerical_sentiment': 'numerical_sentiment_all'})
   topic_sentiment_sem = topic_sentiment_sem.rename(columns={'numerical_sentiment': 'numerical_sentiment_all_sem'})
   topic_high_conf_avg = topic_high_conf_avg.rename(columns={'numerical_sentiment': 'numerical_sentiment_high_conf'})
   topic_high_conf_sem = topic_high_conf_sem.rename(columns={'numerical_sentiment': 'numerical_sentiment_high_conf_sem'})

   topic_sentiment = pd.merge(topic_sentiment_avg, topic_sentiment_sem, on='topic', how='outer')
   topic_high_conf = pd.merge(topic_high_conf_avg, topic_high_conf_sem, on='topic', how='outer')
   all_data = pd.merge(topic_sentiment, topic_high_conf, on='topic', how='outer')

   x = range(len(focus_topics))
   width = 0.35

   for i, (topic_key, topic_label) in enumerate(focus_topics.items()):
       row = all_data[all_data['topic'] == topic_key]
       if row.empty:
           ax.text(i + width/2, 0, 'X', color='red', ha='center', va='center', fontsize=20, fontweight='bold')
           continue
           
       sentiment_all = row['numerical_sentiment_all'].values[0] if not row.empty else np.nan
       sentiment_high = row['numerical_sentiment_high_conf'].values[0] if not row.empty else np.nan
       
       color_all = get_color_gradient(sentiment_all)
       color_high = get_color_gradient(sentiment_high)
       
       if not pd.isna(sentiment_all):
           ax.bar(i, sentiment_all, width, yerr=row['numerical_sentiment_all_sem'],
                 color=color_all, edgecolor='black')
       if not pd.isna(sentiment_high):
           ax.bar(i + width, sentiment_high, width, yerr=row['numerical_sentiment_high_conf_sem'],
                 color=color_high, hatch='//', edgecolor='black')

   ax.set_xticks([p + width/2 for p in x])
   ax.set_xticklabels([topic_label for topic_key, topic_label in focus_topics.items()], 
                      rotation=45, ha='right')
   ax.set_xlabel('')
   ax.set_ylabel('Avg Sentiment Score')
   ax.set_title(title)
   ax.set_ylim(-1.1, 1.1)

def create_4x2_panel_plot():
   fig, axs = plt.subplots(4, 2, figsize=(6, 8), sharex=True, sharey=True)
   
   countries = ['DE', 'DK', 'NO', 'AT']

   for i, country in enumerate(countries):
       twitter_data = load_data(country, 'twitter')
       headline_data = load_data(country, 'headline')
       
       plot_specific_topics(headline_data, axs[i, 0], f'{country_names[country]} - Headlines')
       plot_specific_topics(twitter_data, axs[i, 1], f'{country_names[country]} - Twitter')

   legend_elements = [
       Rectangle((0,0), 1, 1, facecolor='white', edgecolor='black', label='All data'),
       Rectangle((0,0), 1, 1, facecolor='white', hatch='//', edgecolor='black', label='High confidence')
   ]
   
   fig.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.29, 1.02), ncol=2)
   plt.tight_layout()
   
   plt.savefig('sentiment_analysis.png', bbox_inches='tight', dpi=300)
   plt.close()

create_4x2_panel_plot()


for country in ['DE', 'DK', 'NO', 'AT']:
   twitter_data = pd.read_csv(f'{country}/twitter_sentiment.csv')
   headline_data = pd.read_csv(f'{country}/headline_sentiment.csv')
   
   # Count total
   twitter_total = len(twitter_data)
   headline_total = len(headline_data)
   
   # Count high confidence (>0.8)
   twitter_high_conf = len(twitter_data[twitter_data['sentiment_score'] > 0.8])
   headline_high_conf = len(headline_data[headline_data['sentiment_score'] > 0.8])
   
   print(f'\n{country}:')
   print(f'Twitter: {twitter_total:,} total, {twitter_high_conf:,} high conf ({twitter_high_conf/twitter_total*100:.1f}%)')
   print(f'Headlines: {headline_total:,} total, {headline_high_conf:,} high conf ({headline_high_conf/headline_total*100:.1f}%)')


print('+++++++')


countries = ['DE', 'DK', 'NO', 'AT']
total_twitter = 0
total_headlines = 0
high_conf_twitter = 0
high_conf_headlines = 0

for country in countries:
   twitter_data = pd.read_csv(f'{country}/twitter_sentiment.csv')
   headline_data = pd.read_csv(f'{country}/headline_sentiment.csv')
   
   total_twitter += len(twitter_data)
   total_headlines += len(headline_data)
   high_conf_twitter += len(twitter_data[twitter_data['sentiment_score'] > 0.8])
   high_conf_headlines += len(headline_data[headline_data['sentiment_score'] > 0.8])

print(f'Total Twitter: {total_twitter:,} tweets, {high_conf_twitter:,} high conf ({high_conf_twitter/total_twitter*100:.1f}%)')
print(f'Total Headlines: {total_headlines:,} headlines, {high_conf_headlines:,} high conf ({high_conf_headlines/total_headlines*100:.1f}%)')
