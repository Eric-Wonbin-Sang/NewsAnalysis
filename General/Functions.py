import os


def get_curr_parent_dir(path_addition=None):
    return os.path.dirname(os.getcwd()) + path_addition if path_addition is not None else ""


def get_path_list_from_directory(parent_dir):
    path_list = []
    for path in os.listdir(parent_dir):
        full_path = os.path.join(parent_dir, path)
        if os.path.isfile(full_path):
            path_list.append(full_path)
    return path_list
