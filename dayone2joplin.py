#!/usr/local/bin/python3

import datetime, json, os, pathlib, sys, textwrap, uuid

# Check for less than two arguments passed.
def check_arguments() -> None:
    if len(sys.argv) < 3:
        print("Usage: python3 dayone2joplin.py [source dir] [target dir]")
        exit()


def get_source_json() -> str:
    cwd = os.getcwd() # Get current working directory.
    source_dir = sys.argv[1] # Use first argument.
    return cwd + "/" + source_dir + "/Journal.json"


def get_target_dir() -> str:
    cwd = os.getcwd() # Get current working directory.
    target_dir = cwd + "/" + sys.argv[2] + "/" # Use second argument.
    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True) # Create directory if it doesn't exist.
    return target_dir


def generate_uuid() -> str:
    new_uuid = str(uuid.uuid4())
    new_uuid = new_uuid.replace("-", "") # Remove dashes
    return new_uuid


def write_file(filename: str, content: str) -> None:
    new_file = open(filename, "w+")
    new_file.write(content)
    new_file.close()


def get_location(entry: dict) -> (float, float):
    location = entry.get('location', {'longitude': 0.0, 'latitude': 0.0})
    return location['longitude'], location['latitude']


def get_dates(entry: dict) -> (str, str):
    current_date = datetime.datetime.now() # Get current date and time.
    creation_date = entry.get('creationDate', current_date)
    modified_date = entry.get('modifiedDate', current_date)
    return creation_date, modified_date


def get_self_uuid(entry: dict) -> str:
    default_uuid = generate_uuid()
    uuid = entry.get('uuid', default_uuid).lower()
    return uuid


def get_content(entry: dict) -> str:
    content = entry.get('text', "") # Set entry contents to empty string if not available.
    content = content.replace("\\", "") # Remove all single backslashes displayed.        
    return content


def get_title(text: str) -> str:
    title = text.partition('\n')[0] # Get the first line as the title.
    title = title.replace("#", "").lstrip() # Remove all pound signs and leading whitespace.
    title += "\n\n"
    return title


def get_metainfo(self_id: str, parent_id: str, latitude: float, longitude: float, creation_date: str, modified_date: str) -> str:
    metainfo = """\n
        id: {self_id}
        parent_id: {parent_id}
        created_time: {creation_date}
        updated_time: {modified_date}
        is_conflict: 0
        latitude: {latitude}
        longitude: {longitude}
        altitude: 0.0000
        author: 
        source_url: 
        is_todo: 0
        todo_due: 0
        todo_completed: 0
        source: joplin_desktop
        source_application: net.cozic.joplin-desktop
        application_data: 
        order: 0
        user_created_time: {creation_date}
        user_updated_time: {modified_date}
        encryption_cipher_text: 
        encryption_applied: 0
        markup_language: 1
        is_shared: 0
        type_: 1""".format(self_id=self_id, parent_id=parent_id, creation_date=creation_date, modified_date=modified_date, longitude=longitude, latitude=latitude)
        
    metainfo = textwrap.dedent(metainfo) # Remove added indentation from multiline string.
    return metainfo


def convert_to_markdown(entry: dict, target_dir: str, parent_id: str) -> None:
    longitude, latitude = get_location(entry) # Get location.
    creation_date, modified_date = get_dates(entry) # Get dates.
    self_id = get_self_uuid(entry) # Get ID.
    text = get_content(entry) # Get text content.
    title = get_title(text) # Get title.
    metainfo = get_metainfo(self_id, parent_id, latitude, longitude, creation_date, modified_date) # Get metainfo
    text = title + text + metainfo # Prepend title and append metainfo to text

    # Write to new markdown file.
    new_md = target_dir + self_id + ".md"
    write_file(new_md, text)


if __name__ == '__main__':
    check_arguments()
    source_json = get_source_json()
    target_dir = get_target_dir()

    # Generate parent UUID.
    parent_id = generate_uuid()

    # Open and load Journal.json.
    with open(source_json) as json_file:
        data = json.load(json_file)
        entries = data.get('entries')

        if not entries:
            sys.exit("Error: No entries found in Journal.json")

        for entry in entries: # Go through all journal entries.
            convert_to_markdown(entry, target_dir, parent_id)

    # Create resources folder.
    # Future: Enable automatic convertion of images.
    resource_dir = target_dir + "resources"
    pathlib.Path(resource_dir).mkdir(parents=True, exist_ok=True)

    print("Success!")
