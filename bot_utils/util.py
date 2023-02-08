import datetime
from pathlib import Path
import re


def generate_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")[:-4]


def get_root_path():
    return str(Path(__file__).parent.parent.resolve())


def convert_to_uri(filepath):
    return Path(filepath).as_uri()


def clean_link(link):
    link = re.findall(r'(https?://\S+)', link)[0]
    cleaned_link = re.sub(r'\?.*$', '', link)
    return cleaned_link
