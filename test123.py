import boto3
from boto3.session import Session

session = Session(aws_access_key_id = 'AKIAIEQFN3R2B2R6JMJA',
                  aws_secret_access_key = '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',
                  region_name = 'us-west-2')
s3 = session.resource('s3')
bucket = s3.Bucket('roopesh1')
for obj in bucket.objects.all():
    print obj

