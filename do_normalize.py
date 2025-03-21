import os
import sys
import unicodedata

def normalize_names_recursively(path):
    if os.path.isdir(path):
        # 현재 폴더의 이름을 NFC로 변환
        parent_dir, folder_name = os.path.split(path)
        nfc_name = unicodedata.normalize('NFC', folder_name)
        if folder_name != nfc_name:
            new_path = os.path.join(parent_dir, nfc_name)
            os.rename(path, new_path)
            print(f"Renamed folder: {folder_name} -> {nfc_name}")
            path = new_path  # 경로 업데이트

        # 폴더 안의 항목을 재귀적으로 처리
        print(f"Entering directory: {path}")
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            normalize_names_recursively(item_path)
    elif os.path.isfile(path):
        # 파일 이름을 NFC로 변환
        dir_path, file_name = os.path.split(path)
        nfc_name = unicodedata.normalize('NFC', file_name)
        if file_name != nfc_name:
            os.rename(path, os.path.join(dir_path, nfc_name))
            print(f"Renamed file: {file_name} -> {nfc_name}")
        else:
            print(f"Skipped file: {file_name} (No change)")
    else:
        print(f"Invalid path: {path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path>")
    else:
        target_path = sys.argv[1]
        if os.path.exists(target_path):
            try:
                normalize_names_recursively(target_path)
                print("Normalization completed.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("The specified path does not exist.")
    ##input("Press Enter to exit...")
