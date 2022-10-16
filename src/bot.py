import tweepy
import config
from getwyrquestions import get_unique_ques, formimage
from image_edit import GetWyrResultImg
import time
import requests
from pathlib import Path
import json
from PIL import Image

# setting up agent for twitter api v1
auth = tweepy.OAuthHandler(consumer_key=config.API_KEY,
                           consumer_secret=config.API_KEY_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
bot = tweepy.API(auth)

# setting up agent for twitter api v2
client = tweepy.Client(bearer_token=config.BEARER_TOKEN, consumer_key=config.API_KEY,
                       consumer_secret=config.API_KEY_SECRET, access_token=config.ACCESS_TOKEN, access_token_secret=config.ACCESS_SECRET)

try:
    bot.verify_credentials()
    print("Authenticated to Twitter! (*^_^*)")

except Exception as e:
    print("Error authenticating to twitter (╯‵□′)╯︵┻━┻ : ", e)

if __name__ == "__main__":
    while True:
        #MAKE WYR IMAGE
        form_wyr_image = formimage()
        print("(¬‿¬)",form_wyr_image)

        #POST WYR IMAGE
        wyr_update = bot.update_status_with_media(
            status='Would you rather', filename=Path("resources\wyr_final.png"))

        #POST POLL TO WYR IMAGE
        pol1 = "RED" if len(form_wyr_image[0]) > 24 else form_wyr_image[0]
        pol2 = "BLUE" if len(form_wyr_image[1]) > 24 else form_wyr_image[1]
        print(" (¬‿¬) pols : ",pol1,'  ',pol2)
        wyr_tweet_id = wyr_update.id
        poll_create = client.create_tweet(text="Choose ", in_reply_to_tweet_id=wyr_tweet_id,
                                          poll_options=[pol1, pol2], poll_duration_minutes=720)
        print("WYR tweet made (*^_^*)")
        id1 = poll_create.data["id"]

        #SLEEPING 6 HOURS FOR RESULT AND NEXT POST
        time.sleep(3600*6)

        #GETTING THE POLL AND THE VOTES TO FORM RESULT IMAGE
        j=bot.get_status(id=wyr_tweet_id)
        data_url = f'https://api.twitter.com/2/tweets?ids={id1}&expansions=attachments.poll_ids&poll.fields=duration_minutes,end_datetime,options,voting_status'
        response = requests.get(
            data_url, headers={'Authorization': f'Bearer {config.BEARER_TOKEN}'})
        response_json = json.dumps(response.json())
        poll_json=json.loads(response_json)
        print(poll_json)
        votes = [poll_json['includes']['polls'][0]['options'][0]['votes']+j.favorite_count,
                 poll_json['includes']['polls'][0]['options'][1]['votes']+j.retweet_count]
        print(votes)
        ques = [form_wyr_image[0], form_wyr_image[1]]

        #FORMING RESULT IMAGE
        form_result_img = GetWyrResultImg(
            ch1=ques[0], ch2=ques[1], votes1=votes[0], votes2=votes[1])
        form_result_img.form_result()
       
        # CONVERTING RESULT PNG TO JPEG FOR TWITTER MEDIA_UPLOAD REQUIREMENTS
        im = Image.open(Path("resources/wyr_results/result_wyr.png"))
        rgb_im = im.convert('RGB')
        rgb_im.save(Path('resources/wyr_results/result_wyr_jpeg.jpeg'))
        
        #UPLOADING MEDIA TO TWITTER TO GET MEDIA ID
        file = open(Path('resources/wyr_results/result_wyr_jpeg.jpeg', 'rb'))
        resu=bot.media_upload(filename=Path('resources/wyr_results/result_wyr_jpeg.jpeg'),file=file)
        print(resu.media_id_string)

        #POSTING RESULT BY QUOTING ORIGINAL TWEET
        client.create_tweet(media_ids=[resu.media_id_string], quote_tweet_id=wyr_tweet_id)
