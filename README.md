# Breast cancer classification

Dataset used: [RSNA Screening Mammography Breast Cancer Detection](https://www.https://www.kaggle.com/competitions/rsna-breast-cancer-detection/leaderboard)

## Step to reproduce
1. Run [`dataset_prep` notebook](dataset_prep.ipynb) for creation balanced dataset and exporting file names to load
2. Run [script for partial dataset loading ](kaggle_script.py) to load that data.
3. Parse dicom files into 512x512 images using [`dicom_parsing` notebook](dicom_parsing.ipynb)
4. Extract features from that images with `EfficientNet`, ['feature_extraction' notebook](feature_extraction.ipynb)
5. Finally, run training and results evaluation [notebook](classifiers_training.ipynb)