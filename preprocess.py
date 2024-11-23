import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

df = pd.read_csv('C:/cyber_bullying/positive.csv')
comments = df['Comment'].tolist()

def preprocess_comments(comments):
    comments = [str(comment).lower() for comment in comments if isinstance(comment, str) or isinstance(comment, float) and not pd.isna(comment)]
    comments = [re.sub(r'http\S+|www\S+|https\S+', '', comment, flags=re.MULTILINE) for comment in comments]
    comments = [re.sub(r'\W+', ' ', comment) for comment in comments] 
    stop_words = set(stopwords.words('english'))
    comments = [' '.join([word for word in comment.split() if word not in stop_words]) for comment in comments]
    tokenized_comments = [word_tokenize(comment) for comment in comments]
    lemmatizer = WordNetLemmatizer()
    lemmatized_comments = [[lemmatizer.lemmatize(word) for word in comment] for comment in tokenized_comments]
    cleaned_comments = [[word for word in comment if len(word) > 1] for comment in lemmatized_comments]
    final_comments = [' '.join(comment) for comment in cleaned_comments]
    
    return final_comments

preprocessed_comments = preprocess_comments(comments)
preprocessed_df = pd.DataFrame(preprocessed_comments, columns=['preprocessed_comments'])
output_file_path = 'C:/cyber_bullying/preprocessed_positive.csv'
preprocessed_df.to_csv(output_file_path, index=False) 
print(f"Preprocessed comments saved to {output_file_path}")