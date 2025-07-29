import tweepy
from tweepy import OAuthHandler

consumer_key = 'YOcYsagqHX7CmQhV0tNUlW4K2'
consumer_secret = 'EJrsMeTdknBAJVKQHaWJ1Kbljiw612vfee56eQfwgmTatFBLD6'
access_token = '1803654763180871680-Ojrn9l0gb7bxzHWqOXjiRhcsivUnNM'
access_secret = 'j9IaSxQeH4c62gqb9fdKvQ3l0wUOmkVLsJz2xDbl5O3J6'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAABhu3AEAAAAAdFI9I%2FPZiBPMPdpwGPniN89pMQ8%3DUm7QpBTqzBCOC9F8eH01Pcv9pooojkuYkQAZX6MhCU3CbUJTLH'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

client = tweepy.Client(bearer_token=bearer_token,)

# username = 'kenyasgossips'
username = 'karani37868'
user_response = client.get_user(username=username)
user_id = user_response.data.id

print(f"User ID for @{username} is {user_id}")
