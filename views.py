
from ToDo.models import users,todos

session={}

def signin_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("you must login")
    return wrapper

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password]
    return user

class SignInView:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            print("success")
            session["user"]=user[0]
        else:
            print("invalid")

class ToDoView:
    @signin_required
    def get(self,*args,**kwargs):
        return todos
    @signin_required
    def post(self,*args,**kwargs):
        userid=session["user"]["id"]
        kwargs["userId"]=userid
        todos.append(kwargs)
        print(todos)

class MyToDoListView:
    @signin_required
    def get(self,*args,**kwargs):
        userid=session["user"]["id"]
        my_todo=[todo for todo in todos if todo["userId"]==userid][0]
        return my_todo

class ToDoDetailsView:
    def get_object(self,id):
        todo = [todo for todo in todos if todo["todoId"] == id]
        return todo
    @signin_required
    def get(self,*args,**kwargs):
        todo_id=kwargs.get("todoId")
        todo=self.get_object(todo_id)
        return todo
    @signin_required
    def delete(self,*args,**kwargs):
        todo_id=kwargs.get("todoId")
        data=self.get_object(todo_id)
        if data:
            todo=data[0]
            todos.remove(todo)
            print("post removed")
            print(len(todos))
    @signin_required
    def put(self,*args,**kwargs):
        todo_id=kwargs.get("todoId")
        data=kwargs.get("data")
        instance=self.get_object(todo_id)
        if data:
            todo_obj=instance[0]
            todo_obj.update(data)
            return todo_obj

@signin_required
def logout(*args,**kwargs):
    session.pop("user")



lg=SignInView()
lg.post(username="akhil",password="Password@123")
# print(session)
#
# todo=TodoView()
# print(todo.get())
# todo.post(todoId=9,task_name="bbill",completed=True)
#
# mytodo=MyTodoListView()
# print(mytodo.get())


tododetails=ToDoDetailsView()
# print(tododetails.get(todoId=4))
# tododetails.delete(todoId=5)
data={"task_name":"tv recharge"}
print(tododetails.put(todoId=5,data=data))

logout()
print(session)
