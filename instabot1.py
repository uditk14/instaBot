# importing libraries
import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from Test import get_keywords
from Clarify_Example import get_keywords_from_image

# Access Token and Base URL of Instagram API
APP_ACCESS_TOKEN = '1470977960.d177b11.794aeb1c52f6466389e3836ef0c16b57'
BASE_URL = 'https://api.instagram.com/v1/'

# Access Token and Base URL of ParallelDots API
APP_ACCESS_TOKEN_PD = 'rnaQPDGNt7ZmD8wFa1e3qlDu9SQnEf52ZGdhAJXB8Q0'
BASE_URL_PD = 'https://apis.paralleldots.com/'


# Function for fetching own details
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    # Retrieving and converting the response to json
    user_info = requests.get(request_url).json()
    # Checking the status code of the response
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            # Printing the user information
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function for obtaining user-id from username
def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


# Function for getting other user's information
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


# Function to get own recent post
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# Function to get user recent post
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested

    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# Function to get id of recent post by the user using username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    # print user_media

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


# Function to like a post by user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}

    # Printing the url that is being called/requested
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:

        print 'Your like was unsuccessful. Try again!'


# Function to comment on user's post
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)

    # Printing the url that is being called/requested
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


# function to get list of users who like user's media
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested

    print 'GET request url : %s' % (request_url)
    like_list = requests.get(request_url).json()
    print like_list

    if like_list['meta']['code'] == 200:
        if len(like_list['data']):
            for i in range(0,len(like_list['data'])):
                print 'Username: %s' % (like_list['data'][i]['username'])

        else:
            print 'There is no like for this user media!'
    else:
        print 'Query was unsuccessful!'


# function to get list of comments
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code'] == 200:

        if len(comment_list['data']):
            for i in range(0, len(comment_list['data'])):
                print comment_list['data'][i]['text']
        else:
            print 'There is no comment for this user media!'
    else:
        print 'Query was unsuccessful!'


# function to delete negative comment
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


# Function to post the promotional message requested from user
def post_promotional_comment(insta_promotional_message, insta_username):
    # Fetching recent media id
    media_id = get_post_id(insta_username)
    payload = {"access_token": APP_ACCESS_TOKEN, "text": insta_promotional_message}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    # Printing the url that is being called/requested
    print 'POST request url : %s' % (request_url)

    # Commenting the
    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a promotional comment!"
    else:
        print "Unable to add comment. Try again!"


# function to do marketing
def insta_marketing(insta_keyword,insta_promotional_message,insta_username):
    # Analyze comments
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    print comment_info
    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']):

            for index_var in range(0, len(comment_info['data'])):
                comment_text = comment_info['data'][index_var]['text']
                print comment_text
                comment_words = comment_text.split()
                print comment_words
                for i in range(0,comment_words.__len__()):
                    if(comment_words[i] == insta_keyword):
                        post_promotional_comment(insta_promotional_message,insta_username)
                        break
    else:
        print 'Status code other than 200 received'

    # Analyze tags and captions
    request_url = (BASE_URL+'media/%s?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    # Printing the url that is being called/requested
    print 'GET request url : %s' % (request_url)
    media_data=requests.get(request_url).json()

    if(media_data) is not None:

        print media_data

        if (media_data['meta']['code']== 200):

            if len(media_data['data']['tags']):
                # Fetching the tags on a post
                insta_tag = media_data['data']['tags']
                for index_var in range(0,insta_tag.__len__()):
                    if insta_tag[index_var]==insta_keyword:
                        print insta_tag[index_var]
                        post_promotional_comment(insta_promotional_message,insta_username)
                        break
                    else:
                        print 'Not matched'
            else:
                print 'No tags'


            if  (media_data['data']['caption']) is  not  None:
                # Fetching the captions on a post
                insta_caption = media_data['data']['caption']['text']
                type(insta_caption)
                insta_caption_words = insta_caption.split()

                # using paralleldots to check keywords of caption
                c= insta_caption.encode('ascii','ignore')
                print type(c)
                op_of_func=get_keywords(c ,APP_ACCESS_TOKEN_PD)

                if(len(op_of_func) >0):
                    keywords_in_caption = op_of_func[0]

                    print op_of_func[0]
                    print type(op_of_func)
                    for p in range(0, keywords_in_caption.__len__()):
                        if (keywords_in_caption[p] == insta_keyword):
                            print keywords_in_caption[p]
                            post_promotional_comment(insta_promotional_message, insta_username)
                            break
                        else:
                            print 'Not matched'

                # directly checking all words of caption
                for p in range(0, insta_caption_words.__len__()):
                    if (insta_caption_words[p] == insta_keyword):
                        print insta_caption_words[p]
                        post_promotional_comment(insta_promotional_message, insta_username)
                        break
                    else:
                        print 'Not matched'
            else:
                print 'No caption'
        else:
            'Status code other than 200 received'


#Image processing using Clarifai
        # URL to image
        url_of_image1 =media_data['data']['images']['standard_resolution']['url']
        print type(url_of_image1)
        # Converting the URL of image from UNICODE to ASCII
        url_of_image=url_of_image1.encode('ascii','ignore')
        print type(url_of_image)

        # Calling the function for using Clarifai
        image_keywords=get_keywords_from_image(url_of_image)
        # Printing the returned response
        print image_keywords
        print type(image_keywords)

        arr_of_dict=image_keywords['outputs'][0]['data']['concepts']
        print type(arr_of_dict)
        print arr_of_dict

        # Running a loop to iterate all the keywords
        for i in range(0,len(arr_of_dict)):
            keyword = arr_of_dict[i]['name']
            print keyword
            # Checking the keywords retrieved with the keyword
            if (keyword == insta_keyword):
                print arr_of_dict[i]['name']
                post_promotional_comment(insta_promotional_message, insta_username)
                break
            else:
                print 'Not matched'
    else:
        print 'media doesn\'t exist'

# Function to start the bot and presenting a menu

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.To do marketing using specific keywords"
        print "k. To exit"

        choice=raw_input("Enter you choice: ")

        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice=="g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice=="i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "j":
            insta_keyword = raw_input("Enter the keyword to be searched :")
            insta_promotional_message = raw_input("Enter the text to be commented :")
            insta_username = raw_input("Enter the username :")
            insta_marketing(insta_keyword,insta_promotional_message,insta_username)
        elif choice=="k":
            exit()
        else:
            print "Wrong choice"

start_bot()

