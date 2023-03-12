import inspect
import os, boto3

__all__ = ["WatchSession", "S3Session"]

from typing import Iterable

import dotenv

if dotenv.load_dotenv(dotenv.find_dotenv(".env")):
    ...
else:
    print("Load Fail")


class WatchSession(object):
    storage = os.environ["STORAGE"]

    def __init__(self, bucket=None, **kwargs):
        self.session = boto3.session.Session(**kwargs)
        super().__init__()
        self.bucket = bucket


class S3Session(WatchSession):
    """
    >>> import cxm
    >>> import json
    >>> my_bucket = cxm.S3Session(bucket="box.contextmachine.space")
    >>> json.load(my_bucket.get_object(Key="test.json")["Body"])["cxm"]
    True
    """
    def __init__(self, bucket=None, **kwargs):
        super().__init__(bucket, **kwargs)
        self.s3 = self.session.client(
            service_name='s3',
            endpoint_url=self.storage
        )

    def __getattr__(self, item):
        if item in dir(self.s3):
            obj = self.s3.__getattribute__(item)
            if inspect.ismethod(obj):
                return lambda *args, **kwargs: self.s3.__getattribute__(item)(*args, **kwargs, Bucket=self.bucket)
            else:
                return obj
        else:
            return self.__getattribute__(item)

    def __dir__(self):
        return super().__dir__() + self.s3.__dir__()

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
