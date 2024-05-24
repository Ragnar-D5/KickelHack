from io_functions import read_midi,read_wav,debug_play_np_array

if __name__ == "__main__":
    print(read_midi("test_files/TOUHOU_-_Bad_Apple.mid").instruments)
    rate,data = read_wav("test_files/never_gonna_test.wav")
    debug_play_np_array(data,rate)
