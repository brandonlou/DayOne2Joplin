# DayOne2Joplin

> A Python script to convert notes from the [Day One](https://dayoneapp.com/) note taking app into [Joplin](https://joplinapp.org/).

## Usage

### Exporting Day One notes
1. Open Day One.
2. Select the notes you wish to transfer. Click [here](https://help.dayoneapp.com/en/articles/440668-exporting-entries) for official documentation on exporting entries. Export in `JSON` format.
3. Unzip the downloaded `.zip` file.
4. If your notes contain images, the `.zip` file will contain a directory of the same name. Rename this directory to `from_dayone`. If your notes do not contain images, there will only be a `Journal.json` file. If you are using Day One in a different language, this file will have a different name. In this case, rename it to `Journal.json`.
5. Create a new directory named `from_dayone` and move `Journal.json` into it.

### Using the script
0. Requirements: `python3`
1. Clone this repository: `https://github.com/brandonlou/DayOne2Joplin.git`
2. `cd DayOne2Joplin`
3. Move `from_dayone` into the cloned repository.
4. Run `python3 dayone2joplin.py from_dayone to_joplin`.This creates a new directory inside the current directory named `to_joplin`.

### Importing into Joplin
1. Open Joplin.
2. Click `File -> Export -> RAW - Joplin Export Directory`.
3. Open the `to_joplin` directory.
4. Joplin will create a new notebook called `Imported` containing all of your imported notes!

## Additional Information
* All text formatting including bold, italics, headers, bulleted lists, etc. should be preserved.
* Currently, images will not be converted. Images will have to be manually copy and pasted from Day One into Joplin. Please reach out if there is interest in this functionality and I will look into implementing it.
