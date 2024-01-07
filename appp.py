

from flask import Flask,render_template,request
import requests
import pickle
import random
import numpy as np
l = ['https://tse3.mm.bing.net/th?id=OIP.gXOGzwVIoM8nlyr1NHDCxgHaEK&pid=Api&P=0&h=180',
     'https://tse4.mm.bing.net/th?id=OIP.N5ywkmo_D4M0LrVhbMbg9QHaE_&pid=Api&P=0&h=180',
     'https://tse1.mm.bing.net/th?id=OIP.Ec7_gRH4MbBc9kvGUKJXygHaFY&pid=Api&P=0&h=180',
     'https://tse2.mm.bing.net/th?id=OIP.r4GUSL1VC1RzpsO7SWDW_gHaEK&pid=Api&P=0&h=180',
     'https://tse1.mm.bing.net/th?id=OIP.lJJoGGtG9KNF9zbkAPdZfAHaFO&pid=Api&P=0&h=180',
     'https://tse2.mm.bing.net/th?id=OIP.T5VrsMSmYsOtiirZ-6u2jgHaHa&pid=Api&P=0&h=180',
     'https://tse4.mm.bing.net/th?id=OIP.yHDzv9bupSVYUIBTeqG5eAHaHa&pid=Api&P=0&h=180',
     'https://tse2.mm.bing.net/th?id=OIF.BpV86k1jlKr7hrtKgh2R6g&pid=Api&P=0&h=180']
# lu = random.choice(l)
# 'https://tse4.mm.bing.net/th?id=OIP.5tMbnAnenRTEZWUr2bYozgHaFj&pid=Api&P=0&h=180',
# # 'https://tse2.mm.bing.net/th?id=OIP.Qf5ByIGZDV-C7OLfAHgHAgAAAA&pid=Api&P=0&h=180',
# 'https://tse2.mm.bing.net/th?id=OIP.nXspRGpq3HMWpLd13YdU7AHaFj&pid=Api&P=0&h=180',
# 'https://tse4.mm.bing.net/th?id=OIP.Pife6HXF8ua3VbE_Gss-aQHaHa&pid=Api&P=0&h=180',

new = pickle.load(open('new.pkl','rb'))
newses = pickle.load(open('newses.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# text stack using
# ur approach




req = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=07ce6431517e45c5b04b589c36e5bed6')
data= req.json()
def databaseT():
    L=[]
    for i in range(0, 20):
        L.append(data['articles'][i]['title'])

    return L

def databaseA():
    L=[]
    for i in range(0, 20):
        L.append(data['articles'][i]['author'])

    return L

def databaseD():
    L = []
    for i in range(0, 20):
        L.append(data['articles'][i]['description'])

    return L

def databaseI():
    L = []
    urlimage = 'https://static.vecteezy.com/system/resources/previews/000/228/916/original/breaking-news-tv-concept-backdrop-banner-vector.jpg'
    for i in range(0, 20):
        if data['articles'][i]['urlToImage'] == None:
            L.append(urlimage)
        else:
            L.append(data['articles'][i]['urlToImage'])

    return L

def databaseP():
    L = []
    for i in range(0, 20):
        L.append(data['articles'][i]['publishedAt'])

    return L

def databaseU():
    L = []
    for i in range(0, 20):
        L.append(data['articles'][i]['url'])

    return L

listT = databaseT()
listA = databaseA()
listD = databaseD()
listI = databaseI()
listP = databaseP()
listU = databaseU()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           title_name = listT,
                           author = listA,
                           image = listI,
                           votes = listP,
                           rating = listU)

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=["post"])
def recommend():
    user_input = request.form.get('user_input')
    index = new[new['title'] == user_input].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    data = []
    for i in distances[0:30]:
        item = []

        temp_df = newses[newses['Unnamed: 0.1'] == new.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Unnamed: 0.1')['title'].values))
        # item.extend(list(temp_df.drop_duplicates('Unnamed: 0.1')['title_summary'].values))
        item.extend(list(temp_df.drop_duplicates('Unnamed: 0.1')['date'].values))
        item.extend(list(temp_df.drop_duplicates('Unnamed: 0.1')['link'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data, image1 = l)


if(__name__ == '__main__'):
    app.run(debug=True)

