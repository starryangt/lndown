import eel
eel.init("client/dist")

@eel.expose
def hello_world(x):
    print("Hello ", x)

eel.start("index.html")

