from monai.utils import first, set_determinism
from monai.transforms import (
    AsDiscrete,
    AsDiscreted,
    EnsureChannelFirstd,
    Compose,
    CropForegroundd,
    LoadImaged,
    Orientationd,
    RandCropByPosNegLabeld,
    SaveImaged,
    ScaleIntensityRanged,
    Spacingd,
    Invertd,
)
from monai.handlers.utils import from_engine
from monai.networks.nets import UNet
from monai.networks.layers import Norm
from monai.metrics import DiceMetric
from monai.losses import DiceLoss
from monai.inferers import sliding_window_inference
from monai.data import CacheDataset, DataLoader, Dataset, decollate_batch
from monai.config import print_config
from monai.apps import download_and_extract
import torch
import matplotlib.pyplot as plt
import tempfile
import shutil
import os
import glob
from multiprocessing import Pool
import nibabel as nib
import json as json
import numpy as np
import time

start = time.time()
# removing the pre-existing filw
try:
    os.remove("./public_data/file_works.txt")
except:
    print("file is already removed")

# setting directories
root_dir = "./temp/"
print(root_dir)
data_dir = "./public_data/combined/"
train_images = sorted(glob.glob(os.path.join(data_dir, "images", "*.nii.gz")))
train_labels = sorted(glob.glob(os.path.join(data_dir, "labels", "*.nii.gz")))
print(len(train_images), len(train_labels))

# extracting only esophagus
def change(i):
    if "ts_" in i:
        nii_img = nib.load(i)
        nii_data = nii_img.get_fdata()
        if nii_data.max() != 1:
            print(i)
            os.remove(i)
        if nii_data.max() > 1:
            original_affine = nii_img.affine
            array = nii_data
            array[array == 15] = -1
            array[array > 0 ] = 0 
            array[array == -1] = 1.0
            output_nii_img = nib.Nifti1Image(array, original_affine) # Generate an NII image from the segmentation volume and the affine of the input volume
            nib.save(output_nii_img, i)# Save the segmentation NII image
            print(i, "done")
    if "abdomen_" in i:
        nii_img = nib.load(i)
        nii_data = nii_img.get_fdata()
        if nii_data.max() > 1 and np.isin(5, nii_data):
            original_affine = nii_img.affine
            array = nii_data
            array[array == 5] = -1
            array[array > 0 ] = 0 
            array[array == -1] = 1.0
            output_nii_img = nib.Nifti1Image(array, original_affine) # Generate an NII image from the segmentation volume and the affine of the input volume
            nib.save(output_nii_img, i)# Save the segmentation NII image
            print(i, "done")
        if nii_data.max() != 1:
            os.remove(i)
        else:
            print("not inside")
    if "FLARE22" in i:
        nii_img = nib.load(i)
        nii_data = nii_img.get_fdata()
        if nii_data.max() > 1 and np.isin(10, nii_data):
            original_affine = nii_img.affine
            array = nii_data
            array[array == 10] = -1
            array[array > 0 ] = 0 
            array[array == -1] = 1.0
            output_nii_img = nib.Nifti1Image(array, original_affine) # Generate an NII image from the segmentation volume and the affine of the input volume
            nib.save(output_nii_img, i)# Save the segmentation NII image
            print(i, "done")
        if nii_data.max() != 1 :
            os.remove(i)
        else:
            print("not inside")
    else:
        print(i, "already done ")

# multipprocessing to fasten
p = Pool(os.cpu_count() - 2)
with p:
    p.map(change, train_labels)        


train_labels = sorted(glob.glob(os.path.join(data_dir, "labels", "*.nii.gz")))
train_images = sorted(["./public_data/combined/images/" + name for name in os.listdir("./public_data/combined/labels/")])
print(len(train_images), len(train_labels))

print(len(train_images))
train_images1 = []
train_labels1 = []
for x,y in zip(train_images, train_labels):
    if "FLARE" or "ts_" or "abdomen" in x:
        try:
            label = nib.load(y)
            image = nib.load(x)
            array_image = image.get_fdata()
            array = label.get_fdata()
            if array.max() == 1 and array.shape > (96, 96, 96):
                train_labels1.append(y)
                train_images1.append(x)
        except:
            print(x)  

data_dicts = [{"image": image_name, "label": label_name} for image_name, label_name in zip(train_images1, train_labels1)]

train_transforms = Compose(
    [
        LoadImaged(keys=["image", "label"]),
        EnsureChannelFirstd(keys=["image", "label"]),
        ScaleIntensityRanged(
            keys=["image"],
            a_min=-57,
            a_max=164,
            b_min=0.0,
            b_max=1.0,
            clip=True,
        ),
        CropForegroundd(keys=["image", "label"], source_key="image"),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        Spacingd(keys=["image", "label"], pixdim=(1.5, 1.5, 2.0), mode=("bilinear", "nearest")),
        RandCropByPosNegLabeld(
            keys=["image", "label"],
            label_key="label",
            spatial_size=(96, 96, 96),
            pos=1,
            neg=1,
            num_samples=4,
            image_key="image",
            image_threshold=0,
        ),
        # user can also add other random transforms
        # RandAffined(
        #     keys=['image', 'label'],
        #     mode=('bilinear', 'nearest'),
        #     prob=1.0, spatial_size=(96, 96, 96),
        #     rotate_range=(0, 0, np.pi/15),
        #     scale_range=(0.1, 0.1, 0.1)),
    ]
)
val_transforms = Compose(
    [
        LoadImaged(keys=["image", "label"]),
        EnsureChannelFirstd(keys=["image", "label"]),
        ScaleIntensityRanged(
            keys=["image"],
            a_min=-57,
            a_max=164,
            b_min=0.0,
            b_max=1.0,
            clip=True,
        ),
        CropForegroundd(keys=["image", "label"], source_key="image"),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        Spacingd(keys=["image", "label"], pixdim=(1.5, 1.5, 2.0), mode=("bilinear", "nearest")),
    ])

train_files = data_dicts

for i in train_files:
    new_list =[i]
    try:
        check_ds = Dataset(data=new_list, transform=train_transforms)
        check_loader = DataLoader(check_ds, batch_size=1)
        for f in check_loader:
                image, label = (f["image"][0][0], f["label"][0][0])
                print(image.shape)
                print("it worked", i)
                with open("./public_data/file_works.txt", "a") as file: #open will create file
                    file.write(str(i) + "\n")
    except:
        print("this didnt work", i)
        with open("./public_data/not_work.txt", "a" ) as file:
                    file.write(str(i)+ "\n")

end = time.time()

print(f"total time taken is {end - start} seconds")