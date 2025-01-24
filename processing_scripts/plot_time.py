import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

focus_topics = {
    'a_bird_bat': 'bird bat',
    'c_visual': 'visual',
    'f_participation': 'participation',
    'p_long_planning': 'long planning'
}


def plot_sentiment_trends(id_type='twitter'):
    colors = plt.cm.viridis(np.linspace(0, 1, 4))
    topics = ['a_bird_bat', 'c_visual', 'f_participation', 'p_long_planning']
    
    fig, axes = plt.subplots(4, 1, figsize=(12, 16), sharex=True)
    
    for ax_idx, topic in enumerate(topics):
        axes[ax_idx].grid()
        for cc, country in enumerate(['DK', 'DE', 'AT', 'NO']):
            time_col = 'created_at' if id_type == 'twitter' else 'publish_date'
            dat = pd.read_csv(f'{country}/{id_type}_sentiment.csv')
            
            dat['numerical_sentiment'] = dat['sentiment_label'].map({
                'LABEL_0': -1, 'LABEL_1': 0, 'LABEL_2': 1
            })
            
            dat[time_col] = pd.to_datetime(dat[time_col])
            #dat = dat[dat[time_col] >= '2017-01-01']
            
            topic_data = dat[dat['topic'] == topic]
            sentiment_over_time = topic_data.groupby(time_col)['numerical_sentiment'].mean().reset_index()
            sentiment_over_time = sentiment_over_time.sort_values(time_col)
            sentiment_over_time.index = sentiment_over_time[time_col]
            
            mu = sentiment_over_time.numerical_sentiment.rolling('360D', min_periods=1).mean()
            std = sentiment_over_time.numerical_sentiment.rolling('360D', min_periods=1).std()
            N = sentiment_over_time.numerical_sentiment.rolling('360D', min_periods=1).count()
            
            axes[ax_idx].fill_between(sentiment_over_time[time_col], 
                                    mu - std/np.sqrt(N), 
                                    mu + std/np.sqrt(N), 
                                    alpha=0.5, 
                                    facecolor=colors[cc])
            axes[ax_idx].plot(sentiment_over_time[time_col], mu, 
                            lw=4, label=country, c=colors[cc])
            
            # Plot x's on the mean line instead of raw data
            axes[ax_idx].scatter(sentiment_over_time[time_col], 
                               mu,  # Changed from sentiment_over_time.numerical_sentiment
                               marker='x', c=colors[cc], s=80, alpha=0.5)
        
        axes[ax_idx].set_ylim(-1.1, 1.2)
        #axes[ax_idx].set_ylabel('Average Sentiment Score')
        axes[ax_idx].set_xlim(pd.to_datetime('2017-01-01'), pd.to_datetime('2022-12-31'))
        axes[ax_idx].legend(ncol=4, loc='upper left')
        axes[ax_idx].set_ylabel(focus_topics[topic])
        
        if ax_idx == 3:
            axes[ax_idx].set_xlabel('Date')
        
    plt.tight_layout()
    plt.savefig(f"sentiment_trends_{id_type}.png")
    plt.close()

plot_sentiment_trends()
