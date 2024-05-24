from io_functions import read_midi

if __name__ == "__main__":
    print(read_midi("test_files/TOUHOU_-_Bad_Apple.mid").instruments)
