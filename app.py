from flask import Flask, render_template,request
import pickle
import numpy as np


popular_df=pickle.load(open('popular_books.pkl','rb'))
Table=pickle.load(open('Table.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/topbooks')
def topbooks():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author_name=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           rating=list(popular_df['Average Rating'].values),
                           votes=list(popular_df['Total Number of ratings'].values),
                           )


@app.route('/recommend')
def recommendUI():
    return  render_template('recommendUI.html')

@app.route('/recommend_books', methods=['POST'])
def recommendBooks():
    user_input = request.form.get('user_input')
    index = np.where(Table.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == Table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommendUI.html', data=data)

@app.route('/contact')
def Contact():
    return  render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
