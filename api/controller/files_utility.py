from google.cloud import storage


class GCloudStorage:
    def __init__(self, logger, bucket_name):
        self.logger = logger
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def upload_file(self, file_path, content, file_type):
        self.logger.debug(f'Uploading file [{file_path}] to bucket [{self.bucket_name} ')
        try:
            blob = self.bucket.blob(file_path)
            blob.upload_from_string(content, content_type=file_type)
            blob.make_public()
            upload_url = f"https://storage.cloud.google.com/{self.bucket_name}/{file_path}"
            self.logger.debug(f'File [{file_path}] was uploaded successfully')
            return upload_url
        except Exception as e:
            raise

    def delete_file(self, file_path):
        try:
            self.logger.debug(f'Deleting file [{file_path}] to bucket [{self.bucket_name} ')
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_name)
            blob = bucket.blob(file_path)
            blob.delete()
            self.logger.debug(f'File [{file_path}] was deleted successfully')
            return True
        except Exception as e:
            raise

    def check_file_existence(self, file_path):
        try:
            self.logger.debug(f'Searching file [{file_path}] in bucket [{self.bucket_name}')
            found_flag = storage.Blob(bucket=self.bucket, name=file_path).exists(self.storage_client)
            self.logger.debug(f'Searching file [{file_path}] in bucket [{self.bucket_name} was successfull')
            return found_flag
        except Exception as e:
            raise
