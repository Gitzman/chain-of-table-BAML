import os
import pickle
import sys

def pkl_to_txt(input_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.pkl'):
            pkl_path = os.path.join(input_dir, filename)
            txt_path = os.path.join(input_dir, filename[:-4] + '.txt')
            
            with open(pkl_path, 'rb') as pkl_file:
                data = pickle.load(pkl_file)
            
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(str(data))
            
            print(f"Converted {filename} to {filename[:-4]}.txt")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_pkl_to_txt.py <input_directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory")
        sys.exit(1)
    
    pkl_to_txt(input_dir)