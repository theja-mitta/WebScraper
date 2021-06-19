import boto3
import logging
from botocore.exceptions import ClientError
import boto3.session


def is_bucket_exists(bucket_name, region=None):
    exist = False
    try:
        if region is None:
            s3_client = boto3.client('s3')
            if s3_client.head_bucket(Bucket=bucket_name):
                exist = True
    except ClientError as e:
        logging.error(e)
        return False
    return exist


def is_movie_file_exists(bucket_name, file_name):
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, file_name).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print('Oops! file does not exist')
            return False
        else:
            # Something else has gone wrong.
            logging.error('Something has gone wrong')

    print('Found an existing file on s3')
    return True


def get_file_from_s3(bucket, filename, local_filename):
    if is_bucket_exists(bucket):
        if is_movie_file_exists(bucket, filename):
            # get file from s3 to data/current/current.csv
            download_csv_file(bucket, filename, local_filename)
        else:
            print(f"File {filename} doesn't exist on bucket {bucket}")
    else:
        print(f"Bucket {bucket} doesn't exist")
        raise Exception(f"Bucket {bucket} not found")


def push_file_to_s3(filename, bucket, object_name):
    if is_bucket_exists(bucket):
        # get file from s3 to data/current/current.csv
        upload_csv_file(filename, bucket, object_name)
    else:
        print(f"Bucket {bucket} doesn't exist")
        raise Exception(f"Bucket {bucket} not found")


def download_csv_file(bucket, filename, local_filename):
    """Upload a file to an S3 bucket

    :param filename: File to upload
    :param local_filename: Local File for csv to store
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """

    # Downloading the file
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, filename, local_filename)
    except ClientError as e:
        logging.error(e)


def upload_csv_file(filename, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param filename: File to upload
    :param bucket: Bucket to upload to
    :param object_name:
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = filename

    # Uploading the file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(filename, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# def create_bucket(bucket_name='vemitta-datascrape', region=None):
#     """Create an S3 bucket in a specified region
#
#     If a region is not specified, the bucket is created in the S3 default
#     region (us-east-1).
#
#     :param bucket_name: Bucket to create
#     :param region: String region to create bucket in, e.g., 'us-west-2'
#     :return: True if bucket created, else False
#     """
#
#     # Create bucket
#     try:
#         if region is None:
#             s3_client = boto3.client('s3')
#             if s3_client.head_bucket(Bucket='vemitta-datascrape'):
#                 logging.error('Oops! Bucket already exists')
#             else:
#                 s3_client.create_bucket(Bucket=bucket_name)
#         else:
#             s3_client = boto3.client('s3', region_name=region)
#             location = {'LocationConstraint': region}
#             s3_client.create_bucket(Bucket=bucket_name,
#                                     CreateBucketConfiguration=location)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True
