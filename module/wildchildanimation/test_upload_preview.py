from __future__ import print_function
import traceback
import gazu
import sys
import os
import requests
import shutil

def write_log(*args):
    log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)


##############################################################################################################################################################################################
# https://github.com/vsoch/django-nginx-upload/blob/master/push.py
#

from requests_toolbelt.streaming_iterator import StreamingIterator
from requests_toolbelt import (
    MultipartEncoder,
    MultipartEncoderMonitor
)

import requests
import argparse
import hashlib
import sys
import os

def create_callback(encoder):
    encoder_len = int(encoder.len / (1024*1024.0))
    sys.stdout.write("[0 of %s MB]" % (encoder_len))
    sys.stdout.flush()
    def callback(monitor):
        sys.stdout.write('\r')
        bytes_read = int(monitor.bytes_read / (1024*1024.0))
        sys.stdout.write("[%s of %s MB]" % (bytes_read, encoder_len))
        sys.stdout.flush()
    return callback

if __name__ == '__main__':
    email = "paul@wildchildanimation.com"
    password = "Monday@01"
    url = "http://10.147.19.55:8202/edit"
    task_id = "d0f8489b-7907-4377-83df-4fd20e05aaca"
    mode = "preview"
    source_file = "E://Work/WCA/content/KONGOS.mp4"
    source_file = "E://Work/WCA/content/TEST.png"
    # /my_tasks/"

    params = { 
        "username": email,
        "password": password
    } 

    # /edit/logon 
    logon_url = "{}/login/".format(url)
    client = requests.session()

    # Retrieve the CSRF token first
    res = client.get(logon_url).cookies
    csrf = client.get(logon_url).cookies['csrftoken']

    # http://10.147.19.55:8202/edit/login/   
    login_data = dict(username=email, password=password, csrfmiddlewaretoken=csrf, next='/')
    r = client.post(logon_url, data=login_data, headers=dict(Referer=logon_url))

    upload_to = os.path.basename(source_file)
    comments = "Test Upload"
    software = "Maya 2020"

    encoder = MultipartEncoder(fields = { 
        "task_id": task_id,
        "user_id": email,
        "software": software,
        "mode": mode,
        "file_name": upload_to,
        "comment": comments,
        "csrfmiddlewaretoken": csrf,
        'input_file': (upload_to, open(source_file, 'rb'), 'rb')
    })

    progress_callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, progress_callback)
    headers = {'Content-Type': monitor.content_type }

    upload_url = "{}/api/upload/".format(url)
    try:
        r = client.post(upload_url, data=monitor, headers=headers, auth=(email, password))
        print(r.json())
        message = r.json()['message']
        print('\n[Return status {0} {1}]'.format(r.status_code, message))
    except KeyboardInterrupt:
        print('\nUpload cancelled.')
    except Exception as e:
        print(e)



