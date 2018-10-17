import json
import os
import os.path
from cos_utils import CosUtils
from watson_machine_learning_client import WatsonMachineLearningAPIClient


class WatsonStudioUtils:

    def __init__(self, region=None):

        self.cos_credentials = None
        self.wml_credentials = None
        self.cos_utils = None
        self.region = region

    def configure_utilities_from_file(self):

        cos_creds_file = os.path.join("..", "settings", "cos_credentials.json")
        wml_creds_file = os.path.join("..", "settings", "wml_credentials.json")
        if not os.path.isfile(cos_creds_file):
            raise FileExistsError("COS credentials not found at %s" % cos_creds_file)
        if not os.path.isfile(wml_creds_file):
            raise FileExistsError("WML credentials not found at %s" % wml_creds_file)

        with open(cos_creds_file) as json_data:
            cos_credentials = json.load(json_data)
        with open(wml_creds_file) as json_data:
            wml_credentials = json.load(json_data)

        self.configure_utilities(cos_credentials, wml_credentials)

    def configure_utilities(self, cos_credentials, wml_credentials):

        self.cos_credentials = cos_credentials
        self.wml_credentials = wml_credentials

        self.cos_utils = CosUtils(self.cos_credentials, self.region)
        self.wml_client = WatsonMachineLearningAPIClient(self.wml_credentials)
        print("WML client version: %s" % self.wml_client.version)

    def get_cos_utils(self):
        return self.cos_utils

    def get_wml_client(self):
        return self.wml_client

    def get_cos_credentials(self):
        return self.cos_credentials
    
    def save_and_deploy_model(self, trained_model_guid, meta_data_props=None, name, description):
        assert('Not implemented, contact justin.mccoy@us.ibm.com')

    def save_model(self, trained_model_guid, meta_data_props=None):
        # returns saved model guid
        assert('Not implemented, contact justin.mccoy@us.ibm.com')

    def deploy_model(self,model_id, name, description):
        # details of created deployment as a dict
        assert('Not implemented, contact justin.mccoy@us.ibm.com')
