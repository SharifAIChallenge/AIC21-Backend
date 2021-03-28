import random
import string
import requests

from django.conf import settings

from apps.challenge.models import Match, Map


def random_token():
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars)) for i in range(15))


def upload_code(file):
    """
    This function uploads a code file to infrastructure synchronously
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """

    print("ommad upload kone", file.size)
    response = requests.post(
        settings.GATEWAY_HOST + "/upload/code",
        files={'file': file},
        headers={'Authorization': f'Token {settings.GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Upload Code ====")

    return response.json()['code_id']


def upload_map(file):
    print("ommad upload kone", file.size)
    response = requests.post(
        settings.GATEWAY_HOST + "/upload/map",
        files={'file': file},
        headers={'Authorization': f'Token {settings.GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Upload Map ====")

    return response.json()['map_id']


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


def run_match(match: Match):
    response = requests.post(
        settings.GATEWAY_HOST + "/upload/map",
        body={
            'map_id': match.match_info.map.infra_token,
            'player_ids': [
                match.match_info.team1_code.infra_token,
                match.match_info.team2_code.infra_token
            ]
        },
        headers={'Authorization': f'Token {settings.GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Run Game ====")

    return response.json()['game_id']


def run_games(single_games, desired_map):
    """
        Tell the infrastructure to run a list of single_matches (single_match includes tokens,maps,...)
    :param desired_map:
    :param single_games:
    :return: Returns the list of tokens and success status and errors assigned to the matches
    """
    pass


def download_code(file_infra_token):
    response = requests.get(
        settings.GATEWAY_HOST + "/download/code",
        params={
            'code_id': file_infra_token
        },
        headers={'Authorization': f'Token {settings.GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Download File ====")

    return response.json()['url']


def download_log(match_infra_token, file_infra_token=None):

    params = {
        'game_id': match_infra_token
    }
    if file_infra_token:
        params['player_id'] = file_infra_token
    response = requests.get(
        settings.GATEWAY_HOST + "/download/code",
        params=params,
        headers={'Authorization': f'Token {settings.GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Download File ====")

    return response.json()['url']
