from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #o bd vai se chamar esse test.db
db = SQLAlchemy(app)




class ToDo(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      content = db.Column(db.String(200), nullable = False)
      completed = db.Column(db.Integer, default = 0)
      date_create = db.Column(db.DateTime, default = datetime.now)

      def __repr__(self):
            return '<Task %r>' % self.id
            

with app.app_context():
    db.create_all()




@app.route('/',methods = ['POST', 'GET'])

def index():
      if request.method == 'POST':
            #return "Hello, teste da funcao index" #abre uma nova pagina html com isso escrito
            task_content = request.form['content']
            new_task = ToDo(content = task_content)
            #agr tenta inserir no banco de dados
            try:
                  db.session.add(new_task)
                  db.session.commit()
                  return redirect('/')
            except:
                  return "There was an issue adding your task"
      else:
            tasks = ToDo.query.order_by(ToDo.date_create).all()
            return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')

def delete(id):
      task_to_delete = ToDo.query.get_or_404(id) #exclui pela primary key

      try:
            db.session.delete(task_to_delete)
            db.session.commit() #toda vez que estiver usando banco de dados tem que usar o commit, pra deletar ou salvar informacao
            return redirect('/') #volta pra home page
      except:
            return "Item not found in the database, could not be deleted"
      

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
      task = ToDo.query.get_or_404(id)    

      if request.method == 'POST':
            task.content = request.form['content']

            try:
                  db.session.commit() #atualizando no banco de dados
                  return redirect('/')
            except:
                  return "It was not possible to update"
      else:
            return render_template('update.html', task = task)


if __name__== "__main__":
      app.run(debug = True)