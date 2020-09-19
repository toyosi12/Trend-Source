import tweepy
import json
import random
class Fetch:
    result = []
    credentials = {}
    resultType1 = 'popular'
    resultType2 = 'mixed'
    resultCount = 1
    mixedTweetLimit = 200
    lang = "en"
    LAST_ATTENDED_ID_FILE_NAME = 'last_attend_id.txt'
    def __init__(self, _credentials):
        self.credentials = _credentials
        auth = tweepy.OAuthHandler(self.credentials['api_key'], self.credentials['api_secret'])
        auth.set_access_token(self.credentials['access_token'], self.credentials['access_secret'])
        self.api = tweepy.API(auth)


    def search(self, _word):
        #initially fetch the first five most popular tweets, using the 'popular' result type
        popularTweets = self.api.search(_word, result_type = self.resultType1, lang=self.lang, count = self.resultCount)
        if(len(popularTweets) == 0):
            #if there are no popular tweets at the moment, use the 'mixed' result type,
            #loop through to get the tweets with the highest engagements
            popularTweets = self.api.search(_word, result_type = self.resultType2, lang=self.lang, count = self.mixedTweetLimit)
            popularTweets = self.searchAlt(self.toObj(popularTweets))
            print('alternative8')
            return popularTweets
        popularTweets = self.toObj(popularTweets)
        return popularTweets



    def toObj(self, response):
        self.result = [] #empty result for every iteration
        for i in range(len(response)):
            obj = json.loads(json.dumps(response[i]._json))
            self.result.append(obj)
        return self.result


    def searchAlt(self, _tweets):
        tweets = self.sortTweets(_tweets)
        tweets.reverse()
        return tweets[:self.resultCount]


    def sortTweets(self, tweets):
        return sorted(tweets, key=lambda k: k['retweet_count'])



    def getLastAttendedId(self, _fileName):
        fRead = open(_fileName, 'r')
        lastAttendedId = int(fRead.read().strip())
        fRead.close()
        return lastAttendedId

    def saveLastAttendedId(self, _fileName, _lastAttendedId):
        fWrite = open(_fileName, 'w')
        fWrite.write(str(_lastAttendedId))
        fWrite.close()
        return

    def replyToMentions(self, _fileName):
        #Response texts to be selected randomly
        responseTexts = [
                "",
                ""
                ]
        altResponse = "Here is the result of your search "
        responseText = responseTexts[random.randint(0, len(responseTexts) - 1)] + altResponse
        lastId = self.getLastAttendedId(_fileName)
        mentions = self.api.mentions_timeline(lastId, tweet_mode="extended")
        for mention in reversed(mentions):
            myHandle = '@' + self.api.me().screen_name
            responseText = "@" + mention.user.screen_name + " " + responseText
            #In the mention, remove my screen_name(handle) to get the actual
            #word or phrase being searched for
            searchString = mention.full_text.replace(myHandle, "")
            resultTweets = self.search(searchString)
            if(len(resultTweets) == 0):
                return
            # print(mention.user.screen_name + " - " + mention.full_text)
            for r in resultTweets:
                url = "https://twitter.com/" + r['user']['screen_name'] + "/status/" + str(r['id'])
                print(r['user']['screen_name'])
                self.api.update_status(
                            responseText,
                            in_reply_to_status_id=mention.id,
                            auto_populate_reply_metadata=True,
                            attachment_url=url)
                lastId = mention.id
                self.saveLastAttendedId(_fileName, lastId)



    def test(self, _fileName):
        lastId = self.getLastAttendedId(_fileName)
        mentions = self.api.mentions_timeline(tweet_mode="extended")
        for mention in reversed(mentions):
            print('@' + mention.user.screen_name)

            # self.api.update_status('@' + mention.user.screen_name + ' testing' + str(mention.id), mention.id)
            # self.saveLastAttendedId(_fileName, mention.id)






