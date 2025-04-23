import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from box import ConfigBox
from pathlib import Path
from typing import Any, List
import base64


def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads yaml file and returns its content as a ConfigBox."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


def create_directories(path_to_directories: List[Path], verbose: bool = True):
    """Creates list of directories."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


def save_json(path: Path, data: dict):
    """Saves json data to a file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")


def load_json(path: Path) -> ConfigBox:
    """Loads data from a JSON file into a ConfigBox."""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


def save_bin(data: Any, path: Path):
    """Saves binary data to a file."""
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


def load_bin(path: Path) -> Any:
    """Loads binary data from a file."""
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


def get_size(path: Path) -> str:
    """Returns size of file in kilobytes."""
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring: str, fileName: str):
    """Decodes a base64 string and writes it to a file."""
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)


def encodeImageIntoBase64(croppedImagePath: str) -> bytes:
    """Encodes image file to base64 bytes."""
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
