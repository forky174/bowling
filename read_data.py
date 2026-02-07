import numpy as np
import pandas as pd

def read_data(file_id):
    dir = 'bowling/'

    df_raw = pd.read_csv(dir + 'bowling-raw-' + file_id + '.tsv', sep='\t')
    df_raw = df_raw.rename(columns={'# Time': 'time'})
    df_raw = df_raw.rename(columns={'Frame number': 'frame_num'})
    df_raw = df_raw.rename(columns={'X (raw)': 'x'})
    df_raw = df_raw.rename(columns={'Y (raw)': 'y'})
    df_raw = df_raw.drop(0)

    time = np.array(df_raw['time'])
    frame_num = np.array(df_raw['frame_num'])
    x_raw = np.array(df_raw['x'])
    y_raw = np.array(df_raw['y'])

    time = time.astype(np.float32())
    frame_num = frame_num.astype(np.int16())
    x_raw = x_raw.astype(np.float32())
    y_raw = y_raw.astype(np.float32())

    return time, frame_num, x_raw, y_raw