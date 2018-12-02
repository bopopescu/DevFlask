import os
import daemon
cmd = "uwsgi --socket 0.0.0.0:80 --protocol=http --process 4  -w run:app"
os.system(cmd)
