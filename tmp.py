import json
import pendulum
dict = {"Python" : ".py", "C++" : ".cpp", "Java" : ".java"}

try:
    f = open("file.json","rb+")
    x = json.load(f)
    f.close()
except:
    x={}
print x

f = open("file.json","wb")
now = pendulum.now().add(days=-4)
todaysdate = now.date().for_json()
x[todaysdate]=20
x.update(dict)
print x
json.dump(x,f)
print (x)
f.close()