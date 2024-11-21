import tempfile
from minio import Minio
from minio.error import S3Error

class S3Service:
    def __init__(self, endpoint, access_key, secret_key, secure):
        self.client = Minio(endpoint, access_key, secret_key, secure=secure)

    def put_object(self, bucket_name, object_name, file_path):
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"Successfully uploaded {object_name} to {bucket_name}")
        except S3Error as e:
            print(f"Error occurred: {e}")

    def get_object(self, bucket_name, object_name, file_path):
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"Successfully downloaded {object_name} from {bucket_name}")
        except S3Error as e:
            print(f"Error occurred: {e}")
    
    def get_log_file(self, object_name, file_path, bucket_name="projectlogs"):
        # tmp_dir = tempfile.gettempdir()
        try:
            return self.get_object(bucket_name, object_name, file_path)
        except S3Error as e:
            print(f"Error occurred: {e}")
    
    def put_log_file(self, object_name, file_path, bucket_name="projectlogs"):
        try:
            return self.put_object(bucket_name, object_name, file_path)
        except S3Error as e:
            print(f"Error occurred: {e}")
    