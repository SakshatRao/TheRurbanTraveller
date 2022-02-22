import numpy as np
import pickle

phases_data = np.load('./Memories/Processed_Data/phases.npy')
gps_data = np.load('./Memories/Processed_Data/gps_coords.npy')
images_data = np.load('./Memories/Simulated_Data/images.npy')
images_data = np.round(images_data / 30)

memories_dict = {}
for idx in np.arange(phases_data.shape[0]):
    str_idx = f'Phase{idx}'
    memories_dict[str_idx] = {}
    if(phases_data[idx] == 1):
        memories_dict[str_idx]['status'] = 'Travel'
    else:
        memories_dict[str_idx]['status'] = 'Stop'
    memories_dict[str_idx]['gps'] = (gps_data[idx, 0], gps_data[idx, 1])
    memories_dict[str_idx]['images'] = [*np.arange(images_data.shape[0])[images_data == idx]]

pickle.dump(memories_dict, open('./Memories/Processed_Data/memories.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)