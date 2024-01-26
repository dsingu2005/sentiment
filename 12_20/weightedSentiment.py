import pandas as pd

def read_file(file_path):
    return pd.read_excel(file_path)

# Read the files
sentiment_df = read_file("12_20/SampleFolder/CC_AHT LN_Q12023_3_7_2023.xlsx")
keywords_df = read_file("12_20/keywords.xlsx")

# Calculate the total count of keywords in the sentiment DataFrame
total_keywords = sentiment_df['Keyword'].count()

# Calculate the count of each keyword within its category
keyword_counts = keywords_df.groupby('Key Word Category')['Key Words/Topics'].value_counts().reset_index(name='Keyword Count')

# Calculate the ratio of each keyword count to the total keyword count
keyword_counts['Keyword Ratio'] = keyword_counts['Keyword Count'] / total_keywords

# Merge the sentiment DataFrame with the keyword ratios DataFrame
sentiment_df = pd.merge(sentiment_df, keyword_counts, left_on=['Key Word Category', 'Keyword'], right_on=['Key Word Category', 'Key Words/Topics'])

# Calculate the weighted sentiment score
sentiment_df['Weighted Sentiment Score'] = sentiment_df['Sentiment Score'] * sentiment_df['Keyword Ratio']

# Calculate the overall weighted sentiment score for the document
overall_weighted_sentiment = sentiment_df['Weighted Sentiment Score'].sum()

# Print the overall weighted sentiment score
print(f'Overall Weighted Sentiment Score: {overall_weighted_sentiment}')

# Save the DataFrame with the new column to the same Excel file
sentiment_df.to_excel("12_20/SampleFolder/CC_AHT LN_Q12023_3_7_2023.xlsx", index=False)