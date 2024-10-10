import tkinter as tk
from tkinter import scrolledtext
from newspaper import Article
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Download required NLTK data
nltk.download('punkt_tab')
warnings.filterwarnings('ignore')

# Fetch the article content
article = Article('https://en.wikipedia.org/wiki/Bangladesh')
article.download()
article.parse()
article.nlp()
corpus = article.text

# Tokenize the article into sentences
sentence_list = nltk.sent_tokenize(corpus)


# Greeting response
def greeting_response(text):
    text = text.lower()
    bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
    user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


# Sort similarity scores
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index


# Generate bot response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j += 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + " I apologize, I don't understand."

    sentence_list.remove(user_input)
    return bot_response


# Create the GUI
def send():
    user_input = entry_box.get().strip()  # Correctly get single line input
    entry_box.delete(0, tk.END)  # Clear the entry box after input

    if user_input.lower() in ['exit', 'see you later', 'bye', 'quit', 'break']:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Que: " + user_input + '\n')
        chat_log.insert(tk.END, "Ans: Chat with you later!\n\n")
        chat_log.config(state=tk.DISABLED)
        return

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Que: " + user_input + '\n')

    if greeting_response(user_input) is not None:
        bot_answer = greeting_response(user_input)
    else:
        bot_answer = bot_response(user_input)

    chat_log.insert(tk.END, "Ans: " + bot_answer + '\n\n')
    chat_log.config(state=tk.DISABLED)


# Set up the main window
root = tk.Tk()
root.title("Wikipedia Bangladesh")

chat_log = scrolledtext.ScrolledText(root, bd=0, bg="white", height="10", width="56", font="Arial")
chat_log.config(state=tk.DISABLED)

entry_box = tk.Entry(root, bd=0, bg="white", width="30", font="Arial")  # Changed to Entry widget for single line input
send_button = tk.Button(root, text="Send", command=send)

# Layout of widgets
chat_log.grid(row=0, column=0, columnspan=2)
entry_box.grid(row=1, column=0)
send_button.grid(row=1, column=1)

# Start the main loop
root.mainloop()
