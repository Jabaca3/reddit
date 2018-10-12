import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
from _overlapped import NULL
from numpy.core.multiarray import empty
import datetime
from idlelib.iomenu import encoding

reddit = praw.Reddit(client_id='QUhIHM5YT4hDrg',
                     client_secret='6pd3nW3I_atkHoId0bq_qT1NJXc',
                     user_agent='Joseph Baca'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

#These lists are global variables in order to organize the thread(url) to make it more easily accessable
#Some contain specific comments, others contain time frame

timeListAll=[]
allList=[]

posList =[]
posTimeList=[] 

negList =[]
negTimeList=[] 

neuList =[]
neuTimeList=[] 


#given code:---------------------------------------------
def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments
#--------------------------------------------------------


def insert_correct_time_list(emotion,date): #inserts the time into its proper time list
    
    if emotion == 'pos':
        timeListAll.append(date)
        posTimeList.append(date)
    if emotion == 'neg':
        timeListAll.append(date)
        negTimeList.append(date)
    if emotion == 'neu':
        timeListAll.append(date)
        neuTimeList.append(date)
        


def organize_comments(comments):    # inserts the comments into their proper comment list
    positive = get_text_positive_proba(comments)
    negative = get_text_negative_proba(comments)
    neutral =  get_text_neutral_proba(comments)
    
    if positive> max(negative,neutral):
        posList.append(comments)
        allList.append(comments)
        return 'pos'
    
    if negative> max(neutral,positive):
        negList.append(comments)
        allList.append(comments)
        return 'neg'   
    
    if neutral> max(negative, positive):
        neuList.append(comments)
        allList.append(comments)
        return 'neu'
    
    


def process_comments(comments):
    
    for i in range(len(comments)):
        
        emotion = organize_comments(comments[i].body)   #gets the emotion while inserting the comment into a list
        date = get_date(comments[i])                    #gets the date of the comment
        insert_correct_time_list(emotion, date)         #inserts the date into its proper emotion list
        
        try:
            process_comments(comments[i].replies)       #the recursive call to traverse the Btree
        except:
            None
    
            
def get_date(submission):     #extracts the date directly from the thread of the comment
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

def get_oldest_comment_any():
    
    index=0
    oldest=timeListAll[0]
    
    for i in range(1, len(timeListAll)):     #traverses the indecies in the date list and extracts the index from the commnets list
        if timeListAll[i] < oldest:
            index = i
            oldest = timeListAll[i]
            
                
    comment =allList.pop(index)
    date = timeListAll.pop(index)
        
    return comment,date
        
def get_oldest_positive_comment():
    index=0
    oldest=posTimeList[0]
    for i in range(1,len(posTimeList)): #traverses the indecies in the date list and extracts the index from the commnets list
        if posTimeList[i] < oldest:
            oldest = posTimeList[i]
            index = i
                
    comment =posList.pop(index)
    date = posTimeList.pop(index)
        
    return comment,date

def get_oldest_negative_comment():
    index=0
    oldest=negTimeList[0]
    for i in range(1,len(negList)): #traverses the indecies in the date list and extracts the index from the commnets list
        if negTimeList[i] < oldest:
            oldest = negTimeList[i]
            index = i
                
    comment =negList.pop(index)
    date = negTimeList.pop(index)
        
    return comment,date
      
      
      
      
      
      
def main():
    print()
    
    comments = get_submission_comments('https://www.reddit.com/r/AskReddit/comments/9h4plq/how_come_its_a_headline_when_bert_and_ernie_are/') #28 comment sample
    #comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/') #200 comment sample
    #comments = get_submission_comments('https://www.reddit.com/r/AskReddit/comments/9h9kd6/serious_redditors_who_knew_murderers_before_they/') #782 comment sample 
    
    process_comments(comments)  # the function process_comments Extracts the comments from the url and sorts them based on the emotions of the comment by using the organize_comments function
    

    
    
    
    #try:
    #All 3 requested Lists
    print('Positive Comments:')
    print(*posList, sep="\n")
    print('------------------------------------------------------------------------------------')
    print('Negative Comments:')
    print(*negList, sep="\n")
    print('------------------------------------------------------------------------------------')
    print('Neutral Comments:')
    print(*neuList, sep="\n")
    
    #except: None
    
    '''
    #Extra credit
    print(*get_oldest_comment_any())
    print(*get_oldest_positive_comment())
    print(*get_oldest_negative_comment())
    '''

main()
