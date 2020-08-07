#!/usr/local/bin/python3

import json, os, pathlib, sys, tarfile, textwrap, uuid

# Check for less than two arguments passed.
if len(sys.argv) < 2:
    print("Usage: python3 dayone2joplin.py [source dir]")
    exit()

# Get current working directory.
cwd = os.getcwd()

# First argument is source directory relative to cwd.
source_dir = sys.argv[1]
source_json = cwd + "/" + source_dir + "/Journal.json"

# Create target directory if it does not exist.
target_dir = cwd + "/Import/"
pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

# Generate parent UUID.
parent_id = str(uuid.uuid4())
parent_id = parent_id.replace("-", "") # Remove dashes.

with open(source_json) as json_file:
    data = json.load(json_file)
    for entry in data['entries']: # Go through all journal entries.

        # Get location.
        location = entry['location']
        longitude = location['longitude']
        latitude = location['latitude']

        # Get dates.
        creation_date = entry['creationDate']
        modified_date = entry['modifiedDate']

        # Get ID.
        self_id = entry['uuid'].lower()

        # Get text content.
        text = entry['text']
        text = text.replace("\\", "") # Remove all single backslashes displayed.
        title = text.partition('\n')[0] # Get the first line as the title.
        title = title.replace("#", "").lstrip() # Remove all pound signs and leading whitespace.
        text = title + "\n\n" + text # Prepend title to text.

        # Create meta-information.
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

        # Append meta-information to content text.
        text += metainfo

        # Write to new markdown file.
        new_md_name = target_dir + self_id + ".md"
        new_md = open(new_md_name, "w+")
        new_md.write(text)
        new_md.close()

# Create resources folder.
# Future: Enable automatic convertion of images.
resource_dir = target_dir + "resources"
pathlib.Path(resource_dir).mkdir(parents=True, exist_ok=True)

print("Success!")