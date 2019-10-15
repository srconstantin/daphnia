#!/usr/bin/python3.6

import boto
import boto.s3
import boto3
import boto3.s3
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
from boto3.s3.transfer import TransferConfig

#This script uses the library boto to upload files from a provided directory to an AWS S3 instance.
#It uploads the jpeg images captured by the camera to the s3 instance daphniavideo on AWS.


#flag variable for printing information to stdout.
debug = True

def upload_all(directory):
    #sets a transfer configuration, with the specified number of maximum concurrent requests, and fetches s3 credentials from ~/.aws (for root)
    config = TransferConfig(max_concurrency=20)
    s3 = boto3.client('s3')

    files = os.listdir(directory)
    for img in files:
        if debug == True:
             print('upload start')
        path = directory + '/' + img
        #upload image to bucket daphniavideo
        s3.upload_file(path, 'daphniavideo', img, Config=config)
        if debug == True:
            print('image upload complete')

#upload_all('20190617T184936')



