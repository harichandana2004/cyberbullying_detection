import praw
import pandas as pd

def initialize_reddit(client_id, client_secret, user_agent):
    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent=user_agent)

def fetch_submission_comments(reddit, submission_url):
    submission = reddit.submission(url=submission_url)
    submission.comments.replace_more(limit=None)  
    comments = [comment.body for comment in submission.comments.list()]   
    return comments

def save_comments_to_csv(comments, file_name="reddit_comments2.csv"):
    df = pd.DataFrame(comments, columns=["Comment"])
    df.to_csv(file_name, index=False)
    print(f"Comments successfully saved to '{file_name}'.")

if __name__ == "__main__":
    client_id = "YaQTdoYsue9Wri9Dj53DCQ"
    client_secret = "mR4iIri6XyIqbsFiv19HJhlRavXvIA"
    user_agent = "cyberbullying_detector"
    reddit = initialize_reddit(client_id, client_secret, user_agent)
    submission_url = "https://www.reddit.com/r/pics/comments/1g4rtnh/donald_trump_side_angle_from_his_rally_in/"
    comments = fetch_submission_comments(reddit, submission_url)
    if comments:
        save_comments_to_csv(comments, "reddit_comments2.csv")
    else:
        print("No comments found.")
