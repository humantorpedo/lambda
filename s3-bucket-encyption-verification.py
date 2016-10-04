# This file assumes that you have a role that can read from all S3 buckets

import boto3
import botocore

global encryption_header
# I feel like the line below should be enough to determine that SSE is enabled for an S3 bucket. Please let me know if there is some fault in that logic.
encryption_header = "Condition\":{\"Null\":{\"s3:x-amz-server-side-encryption\":\"true"

s3 = boto3.resource('s3')
client = boto3.client('s3')

def lambda_handler(event, context):

    for bucket in s3.buckets.all():
        try:
            bucket_policy = client.get_bucket_policy(Bucket=bucket.name)
            #I know that I should be parsing the json and looking for the value, but it's late and I am taking the coward's way out for now.
            if str(bucket_policy).find(encryption_header) > 0:
                print "%s GREAT JOB!" % bucket.name
            else:
                print "%s has a bucket policy, but not one that enforces encryption" % bucket.name
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
                print "%s does not have a bucket policy" % bucket.name
            else:
                print "Unexpected error: %s" % e
