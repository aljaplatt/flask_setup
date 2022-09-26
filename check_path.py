import os, sys 
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    print('UP: ',user_paths)
except KeyError:
    user_paths = []

print(sys.path)
print('SYS', sys.executable)