#Mbowen CPT135 python final project

#http://praw.readthedocs.io found a bunch of help here
import praw
import tkinter
import tkinter.messagebox
from tkinter import *
from praw.exceptions import APIException
import pickle

class BotCommander(Frame):
    """window for control/feedback"""
    
    def __init__(self):
        """configure window size"""
        Frame.__init__(self)
        self.master.config(bd=5,)
        self.master.title("Repeat After Me Bot")
        self.master.geometry("800x550")
        self.grid()
        
        self.information=Listbox(self, height=20, width=75)
        self.information.grid(row=0, column=0, columnspan=2)
        
        self.which_subreddit_label=Label(text='Which subreddit do you want to get?')
        self.which_subreddit_label.grid(row=1, column=1, sticky='w')

        self.which_subreddit_entry=Entry()
        self.which_subreddit_entry.grid(row=1, column=2, sticky='e')
        
        self.get_new_post_button=Button(text='BOT START', command=self.botstart)
        self.get_new_post_button.grid(row=2, column=0, sticky='w')
        
        
        self.snoo_pic=PhotoImage(file='snoo_pic.gif')
        self.see_a_pic_label=Label(image=self.snoo_pic)
        self.see_a_pic_label.grid(row=3, column=0)
                
    def botstart(self):
        """this is the function for the *botstart* button...makes it all happen"""
        self.information.insert('end', 'reading reddit, looking for someone to repeat after....')                                                                        
        reddit = praw.Reddit('repeat_after_me_bot')                                       #praw is a reddit bot helper file
        chosen_subreddit=self.which_subreddit_entry.get()                                 #subreddit we will troll is gotten from the chosen_subreddit_entry
        try:
            checked_comments=reddit.subreddit(chosen_subreddit).stream.comments()               #this is called the comment stream from the reddit api
        except TypeError:
            self.information.insert('end', 'did you forget to tell me the subreddit?')

        with open ('posts_replied_to.txt', 'r') as posts_replied_to:          
                replies = posts_replied_to.read().split(',')
        for comment in checked_comments:                                                  #loop through all of the comments in the comment stream
            comment.body = comment.body.lower()                                           #encode/decode yet (emojis were messing me up)
            if comment in replies:
                pass
            elif comment.body.startswith('repeat after me'):                            #if comment starts with repeat after me
                self.information.insert('end', 'reddit comment found...')
                try:
                    comment.reply(comment.body)
                    replies.append(comment)
                    print(replies) #for debug
                    with open ('posts_replied_to.txt', 'a')as posts_replied_to:
                        posts_replied_to.seek(0,2)
                        posts_replied_to.write(str(comment)+',')                                                   
                    self.information.insert('end', 'bot has replied, we did it!')
                except APIException:
                    self.information.insert('end', 'you have to wait ten minutes between replies right now...')
                break                                                             #reddit only allows one post every 10min so...break if did it

BotCommander().mainloop()    