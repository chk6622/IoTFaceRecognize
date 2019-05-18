import os, time, uuid
from datetime import datetime




def get_store_file_path(file_name=None):
    folder_name='photoes'
    full_path=None
    if file_name:
        full_path=os.path.join(os.getcwd(),folder_name,file_name)
    return full_path

def get_unknown_photo_file_path():
    return get_store_file_path('%s.jpg' % str(uuid.uuid4()))

def format_date_time(datetime,org_format,dist_format):

    return time.strftime(dist_format, time.strptime(datetime, org_format))

a=datetime.now()

b=datetime.strptime('20190518143605','%Y%m%d%H%M%S')
def get_time_diference(datetime1, datetime2):
    return (datetime2-datetime1).seconds

def get_frame_time_difference(frame_time):
    cur_time = datetime.now()
    frame_time = datetime.strptime(frame_time, '%Y%m%d%H%M%S')
    return get_time_diference(frame_time, cur_time)

# print(format_date_time('20160101152306','%Y%m%d%H%M%S','%Y-%m-%d %H:%M:%S'))
# print(get_frame_time_difference('20190518143605'))