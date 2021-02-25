import datetime
import random
import string
from typing import List

import requests


def random_token():
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars)) for i in range(15))


def upload_file(file):
    """
    This function uploads a file to infrastructure synchronously
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """
    pass


def upload_file_with_url(file):
    """
    This function uploads a file to infrastructure synchronously
    Site will be as server and infrastructure will download it 
    with the url came from site
    
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """
    pass


def download_file(file_token):
    """
    Downloads file from infrastructure synchronously
    :param file_token: the file token obtained already from infra.
    :return: sth that TeamSubmission file field can be assigned to
    """
    pass


def compile_submissions(submissions):
    """
        Tell the infrastructure to compile a list of submissions
    :return: list of dictionaries each have token, success[, errors] keys
    """
    pass


def run_games(single_games, desired_map):
    """
        Tell the infrastructure to run a list of single_matches (single_match includes tokens,maps,...)
    :param desired_map:
    :param single_games:
    :return: Returns the list of tokens and success status and errors assigned to the matches
    """
    pass
