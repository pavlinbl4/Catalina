from PIL import Image
import imagehash
import csv
import os
import shutil
import re

def write_to_csv(image_to_test_full_path, counter):
    with open("simular_images.csv", 'a') as input_file:
        writer = csv.writer(input_file)
        writer.writerow([image_to_test_full_path, counter])

def move_and_copy_file(hr_image, image_to_test_only_name, image_to_test_full_path):
    same_images_folder = f'{os.path.dirname(hr_image)}/look_like_{image_to_test_only_name.split(".")[0]}'
    os.makedirs(same_images_folder, exist_ok=True)
    shutil.move(hr_image, same_images_folder)
    shutil.copy(image_to_test_full_path, f'{same_images_folder}/{image_to_test_only_name}')

def extract_file_name_from_path(image_link):
    return image_link.split('/')[-1]

def compare_images(image_to_test_full_path, hr_image, counter):
    hash0 = imagehash.average_hash(Image.open(image_to_test_full_path))
    hash1 = imagehash.average_hash(Image.open(hr_image))
    cutoff = 10  # maximum bits that could be different between the hashes.
    if hash0 - hash1 < cutoff:
        # print('images are similar')
        counter += 1
        image_to_test_only_name = extract_file_name_from_path(image_to_test_full_path)
        move_and_copy_file(hr_image, image_to_test_only_name, image_to_test_full_path)  # перемещаю похожий файл
    return counter

def all_file_in_folder(folder_path, image_to_test_full_path):
    all_files = os.listdir(folder_path) # all images in "send_folder"
    counter = 0
    for file in all_files:
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".JPG"):
            hr_image = f"{folder_path}/{file}"

            counter = compare_images(image_to_test_full_path, hr_image, counter)
    if counter > 1:
        write_to_csv(image_to_test_full_path, counter)
    print(f' find {counter} similar images')


def go(main_folder):
    print(f'Watch for "JPG" files in {main_folder}')
    for dr in os.listdir(main_folder):
        abs_path = os.path.join(main_folder, dr)  # path to all files in folder
        if os.path.isdir(abs_path):  # if dr is  dir
            go(abs_path)  # recursive work with subfolder
        elif bool(re.match(r'(jpg|jpeg|JPG|JPEG)', dr.split('.')[-1])):
            # print(f'Process {dr} file')
            # print(abs_path)  # full path to image
            image_to_test_full_path = abs_path
            all_file_in_folder("/Volumes/big4photo-4/Отправки/TASS", image_to_test_full_path)


# folder = '/Volumes/big4photo/Documents/TASS/Tass_data'
folder = '/Volumes/big4photo/Documents/TASS/images/2021'
go(folder)



