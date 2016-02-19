import boto3
s3 = boto3.resource('s3')
bucketname = 'roopesh1'
for image in s3.Bucket(bucketname).objects.all():
    imageext = image.key
    imageext = str(imageext)
    print imageext.split('.')[-1]
    if imag