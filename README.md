# Interactive Machine Learning
Aim: The goal of the project is to segment organs from medical slices without much training of the model. To solve this problem we have chosen esophagus as an organ of choice due to its difficult anatomy and segmenation problems

Target: 
1. Collect publicly available annotated datasets where esophagus is available to annotate. here
2. Generate several baselines where models are trained to segment esophagus from the CT images.
3. Test these model on the inhouse dataset that is collected from AIIMS hospital
4. Now, making a tool that is 3d Slicer based
5. Integrating the model based on this paper
6. Validation of the tool

# You can skip steps 1,2,3 if you don't want to train the model

# 0. Installation

`git clone https://github.com/aaekay/iml`
`bash create_environment.sh`

Note: It uses anaconda to install the environment

# 1. Download the datasets

| Serial | Dataset Name | No of files | Link to Download |
| --- | --- | ---- | --- |
| 1 | TotalSegmenatator | 1228 | [Dropbox Link](https://zenodo.org/records/8367088) | 
| 2 | AAPM              | 48   | Link |
| 3 | BTCV              | 30   | [Download abodmen.zip](https://www.synapse.org/#!Synapse:syn3553734) |
| 4 | MICCAI Flare 22 Dataset | 50 | [Link](https://drive.google.com/drive/folders/130DVWqCFALnpHIqnT6aucNIwYygemNjV)

Note: You need to make account at some of the link above to donwload the dataset. Store the dataset in the folder "./public_data/" folder

# 2. Preparing the public dataset
Since, the public datasets contain other organs as well. We will remove the other organs from the segmentation file by retaining only 1 for esophagus and 0 for background.

```bash
conda activate iml
python prepare_public_dataset.py
python preprocess_public_dataset.py

```

# 3. Training the model
Training using UNet architecture model
```bash
conda activate iml
python train_unet.py
```
Training using swin UNETR architecutre model
```bash
conda activate iml
python unetr_eso.py
```


# 4. Use pretrained weights
We are offering pre-trained checkpoints of some models listed below on above datasets. These model were trained on <> datasets. Download these trained model and save it in "./pretrained_cp/

| Architecture | Size | Link to Download |
| ------------ | ---- | ---------------- |
| unet         |      | Link             |
| unetr        |      | Link             |


# 5. Prepare your own dataset
Final file format needed is of .nii (nifti) format. Please convert dicom images into nifti files and store them in the folder "./inhouse_data".

Run this script: <br>
`python pre_processing.py --path ./inhouse_data/` <br>
Note: If you have dicom images, see this description to convert your dicom into .nifti

# 6. Now run the model to generate predictions for esophagus
```bash
conda activate iml
python test.py --ckp <path of checkpoint> --arch <unet or unetr> 
```
Note: architecure choices are unetr or unet

## Todo:

- [x] Add MICCAI Flare dataset
- [ ] add pretrained chekckpoints
- [ ] add statistics and inference time
- [ ] add pictures


# Acknowlegements
1. TotalSegmentator - to provide datasets







