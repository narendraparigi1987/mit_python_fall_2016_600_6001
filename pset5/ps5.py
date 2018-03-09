# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re
import string


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    '''
    class for Data structure design
    '''    
    def __init__(self,guid,title,description,link,pubdate):
        '''
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        '''
        '''
        return self.guid
    
    def get_title(self):
        '''
        '''
        return self.title

    def get_description(self):
        '''
        '''
        return self.description
    
    def get_link(self):
        '''
        '''
        return self.link
    
    def get_pubdate(self):
        '''
        '''
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS
# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self,string):
        '''
        intialization
        '''
        self.phrase = string.lower()
    
    def get_phrase(self):
        '''
        returns phrase
        '''
        return self.phrase

    def is_phrase_in(self,text):
        '''
        checks if phrase is available in text.
        if yes, returns True else False
        does not check if words are sequential or not!!! need fix
        '''
        phrase      = self.get_phrase()
        text        = text
        #replace punctuation with space string
        for i in string.punctuation:
            phrase = phrase.replace(i,' ')
            text   = text.replace(i,' ')
        list_phrase = [phrase.split(' ')[i].lower() for i in range(len(phrase.split(' ')))]
        list_text = [text.split(' ')[i].lower() for i in range(len(text.split(' ')))]
        result = True
        for item in list_phrase:
            if item not in list_text:
                result = False
        return result
    
# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self,string):
        PhraseTrigger.__init__(self,string)
    
    def evaluate(self,story):
        title = story.get_title()
        return self.is_phrase_in(title)

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self,string):
        PhraseTrigger.__init__(self,string)
    
    def evaluate(self,story):
        description = story.get_description()
        return self.is_phrase_in(description)

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self,date_time):
        self.date_time = date_time
    
    def get_time(self):
        date_time = datetime.strptime(self.date_time, "%d %b %Y %H:%M:%S")
        return date_time

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self,time)
    
    def evaluate(self,story):
        pubdate = story.get_pubdate()
        date_time = self.get_time()
        
        try:
            if pubdate < date_time:
                date_time = date_time
        except TypeError:
            date_time = date_time.replace(tzinfo=pytz.timezone("EST"))
        
        if pubdate < date_time:
            return True
        else:
            return False


class AfterTrigger(TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self,time)
    
    def evaluate(self,story):
        pubdate = story.get_pubdate()
        date_time = self.get_time()
        
        try:
            if pubdate > date_time:
                date_time = date_time
        except TypeError:
            date_time = date_time.replace(tzinfo=pytz.timezone("EST"))
            
        if pubdate > date_time:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self,trigger):
        self.trigger = trigger
    
    def get_trigger(self):
        return self.trigger

    def evaluate(self,story):
        trigger = self.get_trigger()
        return not trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self,trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def get_triggers(self):
        return (self.trigger1, self.trigger2)

    def evaluate(self,story):
        (trigger1, trigger2) = self.get_triggers()
        return trigger1.evaluate(story) and trigger2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self,trigger1,trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def get_triggers(self):
        return (self.trigger1, self.trigger2)
    
    def evaluate(self,story):
        (trigger1,trigger2) = self.get_triggers()
        return trigger1.evaluate(story) or trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    result_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                result_stories.append(story)

    return result_stories



#======================
# User-Specified Triggers
#======================
# Problem 11

def help_read_trigger_config(lines):
    '''
    Function: help funcation to create trigger list based on input file
    '''
    trigger_map = {}
    trigger_list = []
    for line in lines:
        list_line = line.split(',')
        if list_line[1] == 'TITLE':
            trigger_map[list_line[0]] = TitleTrigger(list_line[2])
            trigger_list.append(trigger_map[list_line[0]])
        elif list_line[1] == 'DESCRIPTION':
            trigger_map[list_line[0]] = DescriptionTrigger(list_line[2])
            trigger_list.append(trigger_map[list_line[0]])
        elif list_line[1] == 'AFTER':
            trigger_map[list_line[0]] = AfterTrigger(list_line[2])
        elif list_line[1] == 'BEFORE':
            trigger_map[list_line[0]] = BeforeTrigger(list_line[2])
        elif list_line[1] == 'AND':
            trigger_map[list_line[0]] = AndTrigger(trigger_map[list_line[2]],trigger_map[list_line[3]])
        elif list_line[1] == 'OR':
            trigger_map[list_line[0]] = OrTrigger(trigger_map[list_line[2]],trigger_map[list_line[3]])
            trigger_list.append(trigger_map[list_line[0]])
        elif list_line[0] == 'ADD':
            trigger_list.append(trigger_map[list_line[1]])
            trigger_list.append(trigger_map[list_line[2]])
    return trigger_list

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    
    trigger_list = help_read_trigger_config(lines)

    return trigger_list

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t2, t4]

        # Problem 11
        triggerlist = read_trigger_config('debate_triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())
        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()