import os

DB_NAME = "structured"
OUTPUT_COLLECTION = "output"

"""
Utility function to get the model base URL from the environment. 
It attempts to normalize the URL by appending "/v1" to the URL if it is not already present.
:return: the base url of the model server
:raises EnvVarNotSet: if the MODEL_BASEURL environment variable is not set
"""
def get_model_baseurl() -> str:
    if os.getenv("MODEL_BASEURL"):
        url = os.getenv("MODEL_BASEURL")
        if "/v1" in url:
            return url
        else:
            return f"{url}/v1"
    else:
        raise EnvVarNotSet("MODEL_BASEURL environment variable not set")
    

class EnvVarNotSet(Exception):
    pass