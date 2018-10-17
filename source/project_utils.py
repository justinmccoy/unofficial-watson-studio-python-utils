import json
import os
import os.path


class ProjectUtils:

    PROJECT_ID_KEY = "project_id"
    DATA_BUCKET_KEY = "data_bucket"
    RESULTS_BUCKET_KEY = "results_bucket"    

    def __init__(self, studio_utils, project_name):
        self.studio_utils = studio_utils
        self.project_name = project_name.lower()
        self.cos_utils = self.studio_utils.get_cos_utils()

        # Keep the settings independent for each project
        self.settings_directory = os.path.join("./{}".format(project_name), "settings")
        os.makedirs(self.settings_directory, exist_ok=True)

        self.settings_file = os.path.join(self.settings_directory, "project.json")
        if os.path.exists(self.settings_file):
            with open(self.settings_file) as json_data:
                self.settings = json.load(json_data)
                print(self.settings)
                if not self.PROJECT_ID_KEY in self.settings:
                    self.settings[self.PROJECT_ID_KEY] = {}                

                if self.project_name not in self.settings:
                    self.settings[self.project_name] = {}

                if self.DATA_BUCKET_KEY not in self.settings[self.project_name]:
                    print("Creating data bucket")
                    self.data_bucket = self.cos_utils.create_unique_bucket(self.project_name + '-data')
                else:
                    self.data_bucket = self.settings[self.project_name][self.DATA_BUCKET_KEY]
                if self.RESULTS_BUCKET_KEY not in self.settings[self.project_name]:
                    print("Creating results bucket")
                    self.results_bucket = self.cos_utils.create_unique_bucket(self.project_name + '-results')
                else:
                    self.results_bucket = self.settings[self.project_name][self.RESULTS_BUCKET_KEY]

                    
        else:
            print("No project settings found")
            self.settings = {}
            self.settings[self.project_name] = {}
            self.data_bucket = self.cos_utils.create_unique_bucket(self.project_name + '-data')
            self.results_bucket = self.cos_utils.create_unique_bucket(self.project_name + '-results')

        self.settings[self.project_name][ProjectUtils.DATA_BUCKET_KEY] = self.data_bucket
        self.settings[self.project_name][ProjectUtils.RESULTS_BUCKET_KEY] = self.results_bucket

        self.save_project_settings()

    def get_data_bucket(self):
        return self.data_bucket

    def get_results_bucket(self):
        return self.results_bucket

    def get_project_id(self):
        if ProjectUtils.PROJECT_ID_KEY in self.settings:
            if "xxxxx" in self.settings[ProjectUtils.PROJECT_ID_KEY].lower():
                # the placeholder is still present
                return None
            else:
                return self.settings[ProjectUtils.PROJECT_ID_KEY]
        else:
            return None

    def set_project_id(self, project_id):

        self.settings[ProjectUtils.PROJECT_ID_KEY] = project_id
        self.save_project_settings()

    def upload_training_data(self, url, train_datafile_name, save_directory=None):
        # Provide a save directory to rather than delete local downloaded files
        if not save_directory:
            save_directory = os.path.join("./", "data")

        self.cos_utils.transfer_remote_file_to_bucket(url, 
                                                 train_datafile_name, 
                                                 self.data_bucket,
                                                 save_directory=save_directory,
                                                 redownload=False )

        print('\nData uploaded to %s' % self.data_bucket)

    def save_project_settings(self):
        with open(self.settings_file, 'w') as outfile:
            json.dump(self.settings, outfile)
            print('Project settings stored to %s' % self.settings_file)

