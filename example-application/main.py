from config import Config

if __main__ == "__main__":
    config = Config.read()
    download_data()
    process_data()
