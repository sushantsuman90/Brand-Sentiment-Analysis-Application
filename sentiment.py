from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment_vader(text):
    """
    Perform sentiment analysis on the input text using vaderSentiment.

    Parameters:
    - text (str): The input text to analyze.

    Returns:
    - str: 'Positive' if the sentiment is positive, 'Negative' otherwise.
    """

    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Get the polarity score
    sentiment_score = sia.polarity_scores(text)['compound']

    # Determine sentiment based on the compound score
    if sentiment_score >= 0.05:
        return 'Positive'
    elif sentiment_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Example usage:
input_text = "I love this product! It's amazing."
result = analyze_sentiment_vader(input_text)
print(f"Sentiment: {result}")
