# good flask schema: https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
from flask import Flask, render_template, url_for, request, redirect
from flask_migrate import Migrate

# models imports
from shared.models import db
from models.Todo import Todo

# Db settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 slashes: relative path; 4 slashes: absolute path
db.init_app(app)
migrate = Migrate(app, db)

# Flask routes
@app.route('/', methods=['POST', 'GET'])
def index():
    # "request" is available by importing "from flask import request"
    if (request.method == "POST"):
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()        
        return render_template("index.html", tasks=tasks)

@app.route('/todo/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

@app.route('/todo/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if (request.method == "POST"):
        task_content = request.form['content']
        task.content = task_content

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue during updating of your task"
    else:
        return render_template('update.html', task=task)

@app.route('/todo/<int:id>', methods=['GET'])
def getTodo(id):
    if (request.method == "GET"):
        # 1) Getting query params (i.e. ?user=some-value):
        # varUser = request.args.get('user')
        
        # 2) Getting standard HTML form via "application/x-www-form-urlencoded" content type (passed in body)
        # -- OLNY IN POST --
        # -- url send: https://stackoverflow.com/questions/35325370/how-do-i-post-a-x-www-form-urlencoded-request-using-fetch --
        # val = request.form['valName'] # or "request.form.get('valName')"
        
        # 3) Getting "multipart/form-data" content type (passed in body)
        # -- OLNY IN POST --
        # -- url send: https://stackoverflow.com/questions/35192841/how-do-i-post-with-multipart-form-data-using-fetch --
        # -- url encode: https://stackoverflow.com/questions/40414526/how-to-read-multipart-form-data-in-flask --
        # vals = request.form.to_dict() # or "dict(request.form)"
        
        # 4) Getting request body passed in body in JSON format (content type "application/json")
        # -- ONLY IN POST --
        # in js send it using fetch API, in body with usage of JSON.stringify(...) method
        #jsonData = request.json #The request must have the application/json content type
        #jsonData = request.get_json(force=True) #ignores the content type
        #Note1: "jsonData" in dictionary
        #Note2: "loads" from "json" converts json string to Python dictionary
        #Note3: "load" from "json" converts opened json file handle to Python dictionary (file is opened by "open('data.json')")

        # 5) Getting parh variable:
        # We have it in 'id' parameter, but the same is "id = request.view_args['id']"

        # Get item by id
        task = Todo.query.get(id) #optionally filter: "Todo.query.filter(Todo.id==id).first()" or "Todo.query.filter_by(id=id).first()"

        return render_template("task.html", task=task)
        # from: https://stackoverflow.com/questions/13081532/return-json-response-from-flask-view
        #Note:  to return Json data, return stringified dictionary:
        #       return jsonify(data) - "jsonify" is imported from "flask"
        # OR
        #       return Response(dumps(dictData), status=200, mimetype='application/json') - "Response" is imported from flask; "dumps" is imported from "json"
    else:
        return "This url doesn't handle POST method"

if __name__ == "__main__":
    app.run(debug=True)
