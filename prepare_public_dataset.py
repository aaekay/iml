import zipfile
import os
import sys
import glob
import shutil
import time

start = time.time()
# creating the extraction functions for zip and 7z
def unzip_file(zip_file_path, extract_to_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)

#checking the all folder files
folder = "./public_data"
datasets_name = os.listdir(folder)

# creating a combined folder
combined = "./public_data/combined/"
os.makedirs(combined, exist_ok=True)
os.makedirs(os.path.join(combined, "images"), exist_ok=True)
os.makedirs(os.path.join(combined, "labels"), exist_ok=True)

# below are the names of the datasests that you need to download
# datasets = ["Abdomen", "FLARE22", "Totalsegmentator"]

# #checking if all the datasets are downloaded or not
# for i in datasets:
#     for y in datasets_name:
#         if i not in y:
#             raise Exception(f"The dataset {i} is not present in folder public_data. Please download it and save in public_data folder. To download files run bash file download_dataset.sh")

#extracting the files in the respecive folders
for name in datasets_name:
    if ".zip" and "FLARE" in name:
        unzip_file(os.path.join(folder, name), folder)
    if ".zip" and "Totalsegmentator" in name:
        unzip_file(os.path.join(folder, name), os.path.join(folder, "ts"))
    if ".zip" in name and "Abdomen" in name:
        unzip_file(os.path.join(folder, name), folder)

# preparing miccai flare dataset
for name in datasets_name:
    if "FLARE" in name:
        flare = name.split(".")[0]
        print(flare)
flare_folder = os.path.join(folder, flare)
print(flare_folder)
flare_zips = os.listdir(flare_folder)
print(flare_zips)
for name in flare_zips:
    unzip_file(os.path.join(flare_folder, name), os.path.join(flare_folder, name.split(".")[0]))


# for Flare dataset
    
images = glob.glob(f"public_data/{flare}/images/" + "*.nii.gz")
labels = glob.glob(f"public_data/{flare}/labels/" + "*.nii.gz")

print(len(images), len(labels))
for i in images:
    image_name = i.split("/")[-1][:-12]
    #print(image_name)
    os.rename(i, combined + "images/" + image_name + ".nii.gz")
for i in labels:
    label_name = i.split("/")[-1]
    #print(label_name)
    os.rename(i, combined + "labels/" + label_name )

# preparing Abdomen.zip dataset
images = glob.glob("public_data/Abdomen/RawData/Training/img/" + "*.nii.gz")
labels = glob.glob("public_data/Abdomen/RawData/Training/label/" + "*.nii.gz")

try:
    print(len(images), len(labels))
except:
    print("Abdomen dataset is not available. Please download it")
    sys.exit()

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


images = glob.glob("public_data/ts/" + "/**/" "ct.nii.gz")
labels = glob.glob("public_data/ts/" + "/**/" + "segmentations/esophagus.nii.gz")
print(len(images), len(labels))
for i in images:
    image_name = i.split("/")[-2]
    os.rename(i, combined + "images/" + "ts_" + image_name + ".nii.gz")
for i in labels:
    label_name = i.split("/")[-3]
    os.rename(i, combined + "labels/" + "ts_" + label_name + ".nii.gz")




## removing the directories that are not required
dir = [ name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name)) and name != "combined" and ".zip" not in name ]
for name in dir:
    shutil.rmtree(os.path.join(folder, name), ignore_errors=True)


end = time.time()
print(f"the whole script took {start - end} time")