from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful_swagger import swagger

app = Flask(__name__)
# api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1')

app.config['MONGO_DBNAME'] = 'usersdb'

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)
parser.add_argument('username', type=str)

# Todo
#   show a single todo item and lets you delete them
class Todo(Resource):
    "Describing elephants"
    @swagger.operation(
        notes="get a todo item by ID",
        nickname="get",
        # Parameters can be automatically extracted from URLs.
        #   For Example: <string:id>
        # but you could also override them here, or add other parameters.
        parameters=[
            {
                "name": "todo_id_x",
                "description": "The ID of the TODO item",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            },
            {
                "name": "a_bool",
                "description": "The ID of the TODO item",
                "required": True,
                "allowMultiple": False,
                "dataType": "boolean",
                "paramType": "path",
            },
        ],
    )
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

class Authorization(Resource):
    def get(self):
        return 'Hi'

    @swagger.operation(
       notes="Отправка логина для проверки валидности.",
        nickname="auth",
        # Parameters can be automatically extracted from URLs.
        #   For Example: <string:id>
        # but you could also override them here, or add other parameters.
        parameters=[
            {
                "name": "username",
                "description": "Отправка логина для проверки валидности.",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            }
        ] 
    )
    def post(self):
        args = parser.parse_args()
        return args

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')
api.add_resource(Authorization, '/auth')


if __name__ == '__main__':
    app.run(debug=True)