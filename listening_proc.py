import os
import time
from multiprocessing import Process
local_repo_path = '/root/Pictures'
file_count = len(os.listdir(local_repo_path))
def listening_local_repo(path,file_count):
    
    while True:
        cur_files = len(os.listdir(local_repo_path))
        if cur_files != file_count:
            file_count = cur_files
            os.chdir(path)
            os.system('git add .')
            os.system('git commit -m "auto save"')
            os.system('git push ')

        time.sleep(1)
listening_process = Process(target=listening_local_repo, args=(local_repo_path,file_count))
listening_process.start()
