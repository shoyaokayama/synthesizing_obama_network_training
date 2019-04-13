#
# Module to preprocess recording audio files.
#
# ffmpeg must be installed using : "sudo apt install ffmpeg"
# ffmpeg-normalize must be installed using: "pip install ffmpeg-normalize"
# https://github.com/slhck/ffmpeg-normalize
#
import os
import sys

import numpy as np
from scipy.io import wavfile
from mfcc_rev import MFCC


def preprocess(audio_filename, output_filename):
    ext_ind = audio_filename.rfind('.wav')
    audio_filename_formatted = audio_filename[:ext_ind] + '-formatted.wav'
    try:
        os.remove(audio_filename_formatted)
    except OSError:
        pass
    try:
        os.remove(output_filename)
    except OSError:
        pass
    error = os.system(
        'ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar 16000 {}'.format(
            audio_filename, audio_filename_formatted))
    if error:
        raise StandardError('ffmpeg or audio file doesn\'t exist')
    error = os.system(
        'ffmpeg-normalize -f {}'.format(audio_filename_formatted))
    if error:
        raise StandardError('ffmpeg-normalize doesn\'t exist')

    data = wavfile.read(audio_filename_formatted)
    mfcc_inst = MFCC()
    features = mfcc_inst.sig2s2mfc_energy(data[1])

    np.save(output_filename, features)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(
            "Have to pass audio_filename and output_filename as parameters.")
    preprocess(sys.argv[1], sys.argv[2])
