class main:
    def __init__(self) -> None:
        pass
    
    

    def database_post (self, jsonlist):
        import json
        import requests

        post_url = 'https://tributary.svvc.dev/api/upstream/feed'
        for item in jsonlist ["pagelist"]:
            requests.post (post_url, json = item)

        return
    
    #gets article data from the page based on the URL
    def page_scrape (self, url, tag_list):
        from htmldate import find_date
        import time
        import datetime
        
        import metadata_parser
        import requests
        
        #ensures that no error hurts the program
        try:

            r = requests.get (url)
            final_url = str(r.url)
            page = metadata_parser.MetadataParser(final_url)
            
            
            datestr = find_date(final_url)

            dateunix = time.mktime(datetime.datetime.strptime(datestr, "%Y-%m-%d").timetuple())

            
            with open('readme.txt', 'w') as f:
                f.write (str (page.metadata))

            og_data = page.metadata["og"]

            pageobject = {
                "title": og_data ["title"], #required
                "source": og_data ["site_name"],
                "url": og_data ["url"], #required
                "tags": tag_list, #required
                "lat": 2,
                "long": 3,
                "date": dateunix, #not required, do a unix timestamp
                "image": og_data ["image"], #not required, url to image reference
                "description": og_data ["description"], #not required
            }
            
            return pageobject
        except: 
            return None
    
    def tag_gen (self, summary):
        text = summary

        BAD_CHARS = ".!?,\'\""

        # transform text into a list words--removing punctuation and filtering small words
        words = [ word.strip(BAD_CHARS) for word in text.strip().split() if len(word) > 4 ]

        word_freq = {}

        # generate a 'word histogram' for the text--ie, a list of the frequencies of each word
        for word in words :
            word_freq[word] = word_freq.get(word, 0) + 1

        # sort the word list by frequency 
        # (just a DSU sort, there's a python built-in for this, but i can't remember it)
        tx = [ (v, k) for (k, v) in word_freq.items()]
        tx.sort(reverse=True)
        word_freq_sorted = [ (k, v) for (v, k) in tx ]

        temp_ar = []


        for index1 in range (0, len (word_freq_sorted)):
            key_word = word_freq_sorted[index1][0] 
            problem = False
            for index2 in range (index1+1, len(word_freq_sorted)):
                test_word = word_freq_sorted [index2] [0]
                if  test_word in key_word:
                    problem = True

            if not problem:
                temp_ar.append (key_word)

        tag_list = []

        for x in range (0, 3):
            tag_list.append (temp_ar [x])
        
        return tag_list


    #gets list of articles from googly boi
    def google_scrape (self, topic):
        
        #imports google news lib to use
        from pygooglenews import GoogleNews
        gn = GoogleNews()

        #get the list of articles based on topic
        articles = gn.topic_headlines(topic)
        entries = (articles['entries'])

        jsonlist = {
            'pagelist': [],
        }

        for item in entries:
            tag_list = self.tag_gen (item.summary)
            print ("\n\n\n\n======================================")
            print (tag_list)
            jsonlist ['pagelist'].append (self.page_scrape (item.link, tag_list))
        
        return jsonlist
        
    def run (self):
        tecson = self.google_scrape ('Technology')
        buson = self.google_scrape ('Business')
        worldson = self.google_scrape ('World')
        scison = self.google_scrape ('Science')


        self.database_post (tecson)
        self.database_post (buson)
        self.database_post (worldson)
        self.database_post (scison)
        """
        with open('readme.txt', 'w') as f:
            f.write (str (yayson))
            f.write ("===============================================================\n\n\n\n")

        for item in yayson ['pagelist']:
            if (item is not None):
                print (item["title"])
                print (" : ")
                print (item["url"])
        """


        


mn = main()

mn.run()


        