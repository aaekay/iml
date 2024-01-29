import zipfile
import os
import sys
import glob
import shutil


# creating the extraction functions for zip and 7z
def unzip_file(zip_file_path, extract_to_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)

#checking the all folder files
folder = "./public_data"
datasets_name = os.listdir(folder)

# below are the names of the datasests that you need to download
datasets = ["Abdomen.zip", "images.zip", "label.zip" "Totalsegmentator_dataset_v2.zip"]

#checking if all the datasets are downloaded or not
for i in datasets:
    if i not in datasets_name:
        raise Exception(f"The dataset {i} is not present in folder public_data. Please download it and save in public_data folder. To download files run bash file download_dataset.sh")

#extracting the files in the respecive folders
for name in datasets:
    if ".zip" in name:
        unzip_file(os.path.join(folder, name), folder)


# creating a combined folder
combined = "./public_data/combined/"
os.makedirs(combined, exist_ok=True)
os.makedirs(os.path.join(combined, "images"), exist_ok=True)
os.makedirs(os.path.join(combined, "labels"), exist_ok=True)


# preparing Abdomen.zip dataset
images = glob.glob("public_data/Abdomen/RawData/Training/img/" + "*.nii.gz")
labels = glob.glob("public_data/Abdomen/RawData/Training/label/" + "*.nii.gz")
print(len(images), len(labels))

#move the images to a combined folder
for i in images:
    image_name = i.split("/")[-1][3:]
    os.rename(i, combined + "images/" + "abdomen_" + image_name)
for i in labels:
    label_name = i.split("/")[-1][5:]
    os.rename(i, combined + "labels/" + "abdomen_" + label_name)

'''
# preparing abdomen ct1k datset
abdomenct = ["AbdomenCT-1K-ImagePart1", "AbdomenCT-1K-ImagePart2", "AbdomenCT-1K-ImagePart3", "Mask"]
images = []
labels = glob.glob("public_data/Masks/" + "*.nii.gz")
for i in abdomenct:
    if "AbdomenCT" in i:
        temp_list = glob.glob(os.path.join(folder, i) + "/*.nii.gz")
        images.extend(temp_list)
print(len(images), len(labels))

os.makedirs("./public_data/abdomenctk/", exist_ok=True)
image_dir = "./public_data/abdomenctk/"
for i in images:
    name = i.split("/")[-1][:-12] + ".nii.gz"
    os.rename(i, image_dir + name)

images_name = os.listdir(image_dir)

for i in labels:
    name = i.split("/")[-1]
    if name not in images_name:
        raise Exception("Abdomen CT1k dataset in not downloaded properly")
    else:
        os.rename(i, combined + "labels/" + "abdctk_" + name)
        os.rename(image_dir + name, combined + "images/" + "abdctk_" + name )
'''

# for total segmentator dataset
images = glob.glob("public_data/Totalsegmentator_dataset_v2/" + "/**/" "ct.nii.gz")
labels = glob.glob("public_data/Totalsegmentator_dataset_v2/" + "/**/" + "segmentations/esophagus.nii.gz")
print(len(images), len(labels))
for i in images:
    image_name = i.split("/")[-2]
    os.rename(i, combined + "images/" + "ts_" + image_name + ".nii.gz")
for i in labels:
    label_name = i.split("/")[-3]
    os.rename(i, combined + "labels/" + "ts_" + label_name + ".nii.gz")

# preparing miccai flare dataset
images = glob.glob("public_data/images/" + "*.nii.gz")
labels = glob.glob("public_data/labels/" + "*.nii.gz")
print(len(images), len(labels))
for i in images:
    image_name = i.split("/")[-1][:-12]
    #print(image_name)
    os.rename(i, combined + "images/" + image_name + ".nii.gz")
for i in labels:
    label_name = i.split("/")[-1]
    #print(label_name)
    os.rename(i, combined + "labels/" + label_name )



## removing the directories that are not required
dir = [ name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name)) and name != "combined" ]
for name in dir:
    shutil.rmtree(os.path.join(folder, name), ignore_errors=True)


