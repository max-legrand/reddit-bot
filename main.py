from keep_alive import keep_alive
import os
import praw

f = open('output.txt', 'a', 0)

final = "REPLY"

reddit = praw.Reddit(
      client_id=os.getenv("client_id"),
      client_secret=os.getenv("client_secret"),
      password=os.getenv("password"),
      user_agent=os.getenv("user_agent"),
      username=os.getenv("username"))


previous_id = "0"


def search():
    for results in reddit.subreddit('all').comments():
        # Grab all the Recent Comments in every subreddit. This will return 100 of the newest comments on Reddit
        global previous_id
        body = results.body  # Grab the Comment
        body = body.lower()	 # Convert the comment to lowercase so we can search it no matter how it was written
        comment_id = results.id  # Get the Comment ID
        f2 = open("output.txt", "r", 0)
        contents = f2.read()
        if comment_id == previous_id or contents.find(comment_id+"\n")!= -1:  # Check if we already replied to this comment
            print "Already Replied!"
            break

        found = body.find(os.getenv("search"))  # Search for keyword
        if found != -1 and results.author != os.getenv("username"):
            try:
                results.reply(final)  # Reply to the Comment
                f.write(comment_id+"\n")
                f.flush()
                previous_id = comment_id
                print "replied!"
                break
            except Exception:
                print "ERROR!"
                break  # Leave the function if error occurs with replying


keep_alive()
try:
    while 1:

        search()

except KeyboardInterrupt:
    f.close()
