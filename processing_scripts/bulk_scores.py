import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle

# Function to load data based on country and source (Twitter or Headlines)
def load_data(country, ID):
    file_path = f'{country}/{ID}_sentiment.csv'
    return pd.read_csv(file_path)

# Mapping of country codes to full names
country_names = {'DE': 'Germany', 'DK': 'Denmark', 'NO': 'Norway', 'AT': 'Austria'}

# The four specific topics we want to focus on, with their proper names
focus_topics = {
    'a_bird_bat': 'bird bat',
    'c_visual': 'visual',
    'f_participation': 'participation',
    'p_long_planning': 'long planning'
}

# Function to plot specific topics with side-by-side bars for all and high-confidence data
# and handle missing data with red "X" markers
def plot_specific_topics(dat, ax, title, confidence_threshold=0.75):
    # Convert sentiment labels to numerical sentiment
    dat['numerical_sentiment'] = dat['sentiment_label'].map({'LABEL_0': -1, 'LABEL_1': 0, 'LABEL_2': 1})

    # Filter data for the specific focus topics
    dat = dat[dat['topic'].isin(focus_topics.keys())]

    # Group data by topic and calculate mean and standard error for all data
    topic_sentiment_avg = dat.groupby('topic')['numerical_sentiment'].mean().reset_index()
    topic_sentiment_sem = dat.groupby('topic')['numerical_sentiment'].sem().reset_index()

    # Filter high-confidence data
    high_confidence_data = dat[dat['sentiment_score'] > confidence_threshold]
    topic_high_conf_avg = high_confidence_data.groupby('topic')['numerical_sentiment'].mean().reset_index()
    topic_high_conf_sem = high_confidence_data.groupby('topic')['numerical_sentiment'].sem().reset_index()

    # Rename the columns appropriately for merging
    topic_sentiment_avg = topic_sentiment_avg.rename(columns={'numerical_sentiment': 'numerical_sentiment_all'})
    topic_sentiment_sem = topic_sentiment_sem.rename(columns={'numerical_sentiment': 'numerical_sentiment_all_sem'})
    topic_high_conf_avg = topic_high_conf_avg.rename(columns={'numerical_sentiment': 'numerical_sentiment_high_conf'})
    topic_high_conf_sem = topic_high_conf_sem.rename(columns={'numerical_sentiment': 'numerical_sentiment_high_conf_sem'})

    # Merge the standard error and mean for all and high-confidence
    topic_sentiment = pd.merge(topic_sentiment_avg, topic_sentiment_sem, on='topic', how='outer')
    topic_high_conf = pd.merge(topic_high_conf_avg, topic_high_conf_sem, on='topic', how='outer')

    # Merge them together for side-by-side plotting
    all_data = pd.merge(topic_sentiment, topic_high_conf, on='topic', how='outer')

    # Set distinct shades for positive (red) and negative (blue) topics
    red_palette = sns.color_palette("Reds", len(focus_topics))  # Shades of red
    blue_palette = sns.color_palette("Blues", len(focus_topics))  # Shades of blue

    # Plot topics with side-by-side bars
    x = range(len(focus_topics))  # X axis locations for bars
    width = 0.35  # Width of the bars

    # Loop through each topic, and plot data or a red "X" for missing data
    for i, (topic_key, topic_label) in enumerate(focus_topics.items()):
        row = all_data[all_data['topic'] == topic_key]
        if row.empty or pd.isna(row['numerical_sentiment_all']).any():
            # If no data for the topic, place a red "X"
            ax.text(i + width / 2, 0, 'X', color='red', ha='center', va='center', fontsize=20, fontweight='bold')
        else:
            if row['numerical_sentiment_all'].values[0] >= 0:
                ax.bar(i, row['numerical_sentiment_all'], width, yerr=row['numerical_sentiment_all_sem'], label='All data', color=red_palette[i], edgecolor='black')
                ax.bar(i + width, row['numerical_sentiment_high_conf'], width, yerr=row['numerical_sentiment_high_conf_sem'], label='High confidence', color=red_palette[i], hatch='//', edgecolor='black')
            else:
                ax.bar(i, row['numerical_sentiment_all'], width, yerr=row['numerical_sentiment_all_sem'], label='All data', color=blue_palette[i], edgecolor='black')
                ax.bar(i + width, row['numerical_sentiment_high_conf'], width, yerr=row['numerical_sentiment_high_conf_sem'], label='High confidence', color=blue_palette[i], hatch='//', edgecolor='black')

    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels([topic_label for topic_key, topic_label in focus_topics.items()], rotation=45, ha='right')
    ax.set_xlabel('')
    ax.set_ylabel('Avg Sentiment Score')
    ax.set_title(f'Sentiment - {title}')

# Function to create the 4x2 panel plot (4 rows for countries, 2 columns for data types)
def create_4x2_panel_plot():
    fig, axs = plt.subplots(4, 2, figsize=(20, 20), sharex=True, sharey=True)

    countries = ['DE', 'DK', 'NO', 'AT']  # List of countries

    for i, country in enumerate(countries):
        # Load Twitter and Headline data for the country
        twitter_data = load_data(country, 'twitter')
        headline_data = load_data(country, 'headline')

        # Plot specific topics for Headlines and Twitter, assigning subplots
        plot_specific_topics(headline_data, axs[i, 0], f'{country_names[country]} - Headlines')
        plot_specific_topics(twitter_data, axs[i, 1], f'{country_names[country]} - Twitter')

    # Create legend with the correct hatch pattern for high confidence using Rectangle
    all_data_patch = Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', label='All data')
    high_conf_patch = Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', hatch='//', label='High confidence')

    fig.legend([all_data_patch, high_conf_patch], ['All data', 'High confidence'], loc='upper right', frameon=False, ncol=2)

    plt.tight_layout()

    # Save the figure
    plt.savefig('sentiment_specific_topics_4x2_panel_plot_with_x_labels_and_missing_data.png')
    plt.clf()
    plt.close('all')

# Generate the 4x2 panel plot with handling for missing data and shared x-axis
create_4x2_panel_plot()

