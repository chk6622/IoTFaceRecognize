import os, time, uuid




def get_store_file_path(file_name=None):
    folder_name='photoes'
    full_path=None
    if file_name:
        full_path=os.path.join(os.getcwd(),folder_name,file_name)
    return full_path

def get_unknown_photo_file_path():
    return get_store_file_path('%s.jpg' % str(uuid.uuid4()))

print(get_unknown_photo_file_path())