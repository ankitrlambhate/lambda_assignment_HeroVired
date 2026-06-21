import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):

    review = event.get('review', '')

    if not review:
        return {
            'statusCode': 400,
            'body': 'Review text not provided'
        }

    response = comprehend.detect_sentiment(
        Text=review,
        LanguageCode='en'
    )

    sentiment = response['Sentiment']

    print(f"Review: {review}")
    print(f"Sentiment: {sentiment}")

    return {
        'statusCode': 200,
        'review': review,
        'sentiment': sentiment,
        'sentiment_scores': response['SentimentScore']
    }