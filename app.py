from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.utils import secure_filename
import docx
from docx import Document
import pandas as pd
from googletrans import Translator
from google_trans_new import google_translator
import tkinter
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = "thisisasecret"
db = SQLAlchemy(app)
import camelot

class MyForm(FlaskForm):
    file = FileField()
@app.route("/", methods=['GET', 'POST'])
def index():
    form = MyForm()
    # if request.method == 'POST':
    if form.validate_on_submit(): #if post form
        link = request.form['document']
        print(link)
        print(form.file.data)
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        filepath = 'uploads/' + filename
        translate(filepath)
        # extract all the tables in the PDF file
        tables = camelot.read_pdf(link, pages="14,15")
        final = []
        writer = pd.ExcelWriter('file.xlsx')
        for i in range(len(tables)):
            tables[i].df.iloc[1:]
            tables[i].df.columns = [tables[0].df.iloc[0]]
            tables[i].df.drop(index=0, inplace=True)
            tables[i].df.reset_index(inplace=True, drop=True)
            tables[i].df.columns = [tables[0].df.iloc[0]]
            tables[i].df.drop(index=0, inplace=True)
            tables[i].df.reset_index(inplace=True, drop=True)
            final.append(tables[i].df[(tables[i].df == "Asbestos").any(axis=1)]) #select corresponding rows where chemical name matches
        for n, df in enumerate(final):
            df.to_excel(writer,'sheet{}'.format(n))
        writer.save() 
        return f'Filename: {filename}'
    return render_template("index.html", form=form)
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'

#     else:
#         return render_template('update.html', task=task)

def translate(filepath):
    doc = docx.Document(filepath)
    for table in doc.tables:
        doctbls=[]
        tbllist=[]
        rowlist=[]
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                rowlist.append(cell.text)
            tbllist.append(rowlist)
            rowlist=[]
        doctbls=doctbls+tbllist
    df=pd.DataFrame(doctbls)     
    #display(df)
    newbie = []
    newbie.append(df.iloc[1:24, 1]) 
    translator = google_translator()
    translated_var = []
    for i in newbie:
        translated_var.append(translator.translate(i))
    for i in translated_var:
        print(i)
if __name__ == "__main__":
    app.run(debug=True)
