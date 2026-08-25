# Workshop 2.0

A collection of Python tools and experiments for **data processing, web automation, image generation, anomaly detection, and machine learning**.

The repository includes data-processing pipelines, Playwright bots for collecting data, image-processing utilities, and notebooks for anomaly detection using autoencoders and pretrained models.

---

## Repository Structure

```text
workshop2.0/
│
├── data/
|    ├── filterd_sc_bot_csv
|
|
├── data_processing/
│   ├── process_pipeline.py
│   └── ...
│
├── anomaly-detection-our-autoencodr.ipynb
├── anomaly-detection-pretrained-models.ipynb
├── autoencoder-model-build.ipynb
│
├── pics_view.py
│
├── playwright_soundcloud_bot.py
├── playwright_wiki_bot.py
├── playwright_youtube_bot.py
│
├── record_scr.py
│
└── README.md
```

### Main Components

**Data Processing**

The `data_processing` directory contains scripts for parsing, filtering, processing, and preparing collected data.

**Web Automation**

Playwright scripts are used to automate websites such as Wikipedia, YouTube, and SoundCloud.

**Machine Learning**

The repository contains notebooks for experimenting with:

* Convolutional autoencoders
* Pretrained neural-network feature extraction
* Anomaly detection
* Image/histogram representations

---


# Usage Guide
## 1. Record Data Using the Wikipedia Bot

The `record_scr.py` script can be used as a wrapper for Playwright-based recording scripts.

Example:

```powershell
python .\record_scr.py --PythonScript .\playwright_wiki_bot.py --Count 2 --CaptureName basename_of_pacp_&_har --output_dir .\dir_name
```

### Parameters

| Argument         | Description                                   |
| ---------------- | --------------------------------------------- |
| `--PythonScript` | Playwright script that should be executed     |
| `--Count`        | Number of recordings/executions to perform    |
| `--CaptureName`  | Basename assigned to the captured pcap and har data            |
| `--output_dir`   | Directory where the captured output is stored |

at the end the output directory will contain pacp and har with the basename concatenated with number of recording   

## 2. Process Recorded Data

The main processing pipeline can be executed using:

```powershell
python .\data_processing\process_pipeline.py --input_dir .\dir_name --out_file_name FolwPic_Set --parse --TPS 15 --DELTA_T 15
```

### Parameters

| Argument          | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `--input_dir`     | Directory containing the pcap and har files                  |
| `--out_file_name` | Name of the generated output containing all flowpics extracted from Input Directory                       |
| `--parse`         | Enables parsing of the input data                     |
| `--TPS`           | Sliding window length in seconds parameter used for creating flowpics |
| `--DELTA_T`       | Time-difference  between windows in seconds parameter used for creating flowpic     |

### Example

```powershell
python .\data_processing\process_pipeline.py `
    --input_dir .\wiki_bot `
    --out_file_name wiki_bot_all_flowpics `
    --parse `
    --TPS 15 `
    --DELTA_T 15
```
at the end we will get 
```text
input_dir/
│
├── _pics/
|    ├── pic_file_1.npy
|    ├── pic_file_2.npy
|    ├── pic_file_3.npy
│    └── ...
|
├── _unified_pics/
│   ├── out_file_name.npy # it contains all flow pics from  _pics folder
│
├── filterd_csv/
|    ├── filterd_basename_0.csv
|    ├── filterd_basename_1.csv
|    ├── filterd_basename_2.csv
│    └── ...
├── basename_0.csv
├── basename_0.HAR
├── basename_1.csv
├── basename_1.HAR
├── basename_2.csv
├── basename_2.HAR
```
---



# Author

**Nachman Rog**

GitHub: https://github.com/nachman1998

