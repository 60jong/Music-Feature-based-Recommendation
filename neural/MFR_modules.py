# (100, 300, 3)의 output
import librosa
import numpy as np
import librosa.display

from scipy.ndimage import zoom


###################################### Modules

# base y, sr

def ext_base(path):
    y, sr = librosa.load(path)
    return y, sr

# Chroma_stft

def ext_chroma_stft(y, sr):
    chroma_stft = librosa.feature.chroma_stft(y = y, sr = sr)
    chroma_stft = chroma_stft[:,:1200]
    return chroma_stft

# MFCC

def ext_mfcc(y, sr):
    mfcc = librosa.feature.mfcc(y = y, sr = sr)
    mfcc = mfcc[:,:1200]

    return mfcc # 2차원

# Tempogram

def ext_tempogram(y, sr):
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempogram = librosa.feature.tempogram(y=y, sr=sr)
    tempogram = tempogram[:,:1200]
    return tempogram # 2차원

# zoom을 이용한 resizing
def return_zoomed(arr, new_height, new_width):
    zoomed = zoom(arr, (new_height/arr.shape[0], new_width/arr.shape[1]))
    return zoomed


############################################## integrate
# input => 파일 경로
# output => (100, 300, 3)의 데이터 포인트

def ext_datapoint(path):
    y ,sr = ext_base(path)

    feature_list= []

    chroma_stft = ext_chroma_stft(y, sr)
    feature_list.append(chroma_stft)
    mfcc = ext_mfcc(y, sr)
    feature_list.append(mfcc)
    tempogram = ext_tempogram(y, sr)
    feature_list.append(tempogram)

    # 선형 보간 => zoom 방식
    new_height, new_width = 100,300
    for idx, feature in enumerate(feature_list):
        feature_list[idx] = return_zoomed(feature, new_height, new_width)
        feature_list[idx] = np.expand_dims(feature_list[idx], axis = -1)

    #print(f'-------------linear interpolating done--------------')
    #print(f'-------------adding a dimension done--------------')
    #print(f'check!')
    # for x in feature_list:
    #     print(x.shape, end = ' ')
    # print()

    ### concatenate
    concatenated = np.concatenate(feature_list, axis = -1)
    #print(f'-------------concatenating done--------------')
    #print(f'check!')
    #print(f'concatenated.shape : {concatenated.shape}')

    return concatenated


from tensorflow.keras.models import load_model

########################################### (1,H,W,C) return
def ext_sample_input(file_path):
    sample_data = ext_datapoint(file_path)
    sample_data = np.expand_dims(sample_data, axis = 0)
    return sample_data

############################################ 10차원 결과 백터(list) return
def return_result(sample_input, model_path):
    loaded_model = load_model(model_path)
    prediction = loaded_model.predict(sample_input)
    return prediction[0]

############################################ 10차원 결과 백터(list) return <= mk_4부터는 CRNN모델
def return_result_for_crnn(sample_input, model_path):
    loaded_model = load_model(model_path)
    sample_input = np.transpose(sample_input, (0,2,1,3))
    prediction = loaded_model.predict(sample_input)
    return prediction[0]

