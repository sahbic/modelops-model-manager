import yaml
import subprocess
import os
import random
import shutil

import pandas as pd
from pathlib import Path

# SAS Model Manager
import sasctl
from sasctl import Session
from sasctl.services import model_repository, model_management
import sasctl.pzmm as pzmm

def init_folder(model_prefix):
    '''
    Initiate model folder
    '''
    # initiate folder
    MODELS_PATH = 'models'
    MODEL_PATH = MODELS_PATH + '/' + model_prefix

    zipFolder = os.path.join(os.getcwd(), MODEL_PATH)

    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)

    return zipFolder

def read_yaml(filepath):
    '''
    Given file path, Read yaml file 
    :param filepath:
    :return: conn_dict
    '''
    with open(filepath) as file:
        conn_dict = yaml.load(file, Loader=yaml.FullLoader)
    return conn_dict

def write_requirements(folder, filename):
    '''
    Given a folder and the filename, 
    create the requirements file.
    :param folder: 
    :param filename: 
    :return: 
    '''
    reqfile_path = os.path.join(folder, filename)
    with open(reqfile_path, "w") as f:
        sterr = subprocess.call(["pip", "freeze"], stdout=f, stderr=-1)
    if sterr==0:
        print("Requirements file created under " , reqfile_path)
    else:
        print("pip freeze command fails!")

def get_output_variables(names, labels, eventprob):
    '''
    Given variable names, labels and event probability, 
    it creates dataframes for pzmm metadata generation
    :param names: 
    :param labels: 
    :param eventprob: 
    :return: outputVar
    '''
    outputVar = pd.DataFrame(columns=names)
    outputVar[names[0]] = [random.random(), random.random()]
    outputVar[names[1]] = [random.random(), random.random()]
    outputVar[names[2]] = labels
    outputVar[names[3]] = eventprob
    return outputVar

def zip_folder(folder_to_zip_path, rmtree=False):
    '''
    Given the folder to zip path,
    create an archive
    :param folder_to_zip_path: 
    :param rmtree: 
    :return: zipath
    '''
    path_sep = '/'
    root_dir = path_sep.join(folder_to_zip_path.split('/')[:-1])
    base_dir = folder_to_zip_path.split('/')[-1]
    zipath = shutil.make_archive(
        folder_to_zip_path,         # folder to zip
        'zip',                      # the archive format - or tar, bztar, gztar 
        root_dir=root_dir,          # folder to zip root
        base_dir=base_dir)          # folder to zip name
    if rmtree:
        shutil.rmtree(folder_to_zip_path) # remove .zip folder
    return zipath
    
def run_model_tracking (project, model):
    '''
    Given project and model names, 
    create a project and register the model in SAS Model manager
    :param project: 
    :param model: 
    :return: None
    '''
    
    with Session(hostname=SERVER, username=USER, password=PASSWORD, verify_ssl=False):
        #id = uuid.uuid4()
        #uuid_project = project + '_' + str(id)[:8]

        model_repository.create_project(project=project,
                                        repository='Public',
                                        function='classification'
                                        )

        zipfile = open(ZIP_CHAMPION_FOLDER, 'rb')

        model_repository.import_model_from_zip(model,
                                               project,
                                               file=zipfile
                                               )
        zipfile.close()
        
    return 0