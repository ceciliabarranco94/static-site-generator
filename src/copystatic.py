import os
import shutil

def static_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    if os.path.exists(source):
        list_source = os.listdir(source)

        for file in list_source:
            entry_full_path = os.path.join(source, file)
            destination_path = os.path.join(destination, file)
            if os.path.isfile(entry_full_path):
                shutil.copy(entry_full_path, destination_path)
            else:
                static_to_public(entry_full_path, destination_path)