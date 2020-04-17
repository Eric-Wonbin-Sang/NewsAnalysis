import os


from General import Constants


def get_curr_parent_dir(path_addition=None):
    return os.path.dirname(os.getcwd()) + path_addition if path_addition is not None else ""


def get_path_list_from_directory(parent_dir):
    path_list = []
    for path in os.listdir(parent_dir):
        curr_path = os.path.join(parent_dir, path)
        if os.path.isfile(curr_path):
            path_list.append(curr_path)
    return path_list
