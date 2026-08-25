# Workshop 2.0

A collection of Python tools and experiments for **data processing, web automation, image generation, anomaly detection, and machine learning**.

The repository includes data-processing pipelines, Playwright bots for collecting data, image-processing utilities, and notebooks for anomaly detection using autoencoders and pretrained models.

---

## Repository Structure

```text
workshop2.0/
│
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

# Installation

Clone the repository:

```bash
git clone https://github.com/nachman1998/workshop2.0.git
cd workshop2.0
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

Install the main Python dependencies:

```bash
pip install numpy pandas matplotlib scikit-learn torch torchvision opencv-python jupyter playwright
```

Install Playwright browsers:

```bash
playwright install
```

---

# Usage Guide

## 1. Process STS Data

The main processing pipeline can be executed using:

```powershell
python .\python_for_handin\data_processing\process_pipeline.py --input_dir .\python_for_handin\sts\ --out_file_name sc_ok_sts --parse --TPS 15 --DELTA_T 15
```

### Parameters

| Argument          | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `--input_dir`     | Directory containing the input files                  |
| `--out_file_name` | Name of the generated output                          |
| `--parse`         | Enables parsing of the input data                     |
| `--TPS`           | Time-period parameter used by the processing pipeline |
| `--DELTA_T`       | Time-difference parameter used during processing      |

### Example

```powershell
python .\python_for_handin\data_processing\process_pipeline.py `
    --input_dir .\python_for_handin\sts\ `
    --out_file_name sc_ok_sts `
    --parse `
    --TPS 15 `
    --DELTA_T 15
```

The processed data is generated according to the options supplied to the pipeline.

---

## 2. Record Data Using the Wikipedia Bot

The `record_scr.py` script can be used as a wrapper for Playwright-based recording scripts.

Example:

```powershell
python .\python_for_handin\record_scr.py `
    --PythonScript .\python_for_handin\playwright_wiki_bot.py `
    --Count 2 `
    --CaptureName ok_wiki `
    --output_dir .\python_for_handin\sts
```

### Parameters

| Argument         | Description                                   |
| ---------------- | --------------------------------------------- |
| `--PythonScript` | Playwright script that should be executed     |
| `--Count`        | Number of recordings/executions to perform    |
| `--CaptureName`  | Name assigned to the captured data            |
| `--output_dir`   | Directory where the captured output is stored |

### Example

The command above runs the Wikipedia automation script twice and stores the resulting recordings in:

```text
.\python_for_handin\sts\
```

with the capture name:

```text
ok_wiki
```

---

## 3. Record SoundCloud Data

The SoundCloud Playwright script can be executed directly:

```powershell
python .\playwright_soundcloud_test1.py --output_name shishi
```

### Parameters

| Argument        | Description                        |
| --------------- | ---------------------------------- |
| `--output_name` | Name used for the generated output |

### Example

```powershell
python .\playwright_soundcloud_test1.py --output_name shishi
```

This runs the SoundCloud automation script and creates output using `shishi` as its name.

---

# Typical Workflow

A typical workflow for collecting and processing data is:

```text
        Web Automation
              │
              ▼
     Playwright Scripts
              │
              ▼
        Recorded Data
              │
              ▼
      data_processing/
              │
              ▼
       Processed Data
              │
              ▼
       Images / Histograms
              │
              ▼
    Feature Extraction / ML
              │
              ▼
      Anomaly Detection
```

For example:

### Step 1 — Collect data

```powershell
python .\python_for_handin\record_scr.py `
    --PythonScript .\python_for_handin\playwright_wiki_bot.py `
    --Count 2 `
    --CaptureName ok_wiki `
    --output_dir .\python_for_handin\sts
```

### Step 2 — Process the collected data

```powershell
python .\python_for_handin\data_processing\process_pipeline.py `
    --input_dir .\python_for_handin\sts\ `
    --out_file_name sc_ok_sts `
    --parse `
    --TPS 15 `
    --DELTA_T 15
```

### Step 3 — Run ML experiments

Open one of the notebooks:

```text
autoencoder-model-build.ipynb
```

or

```text
anomaly-detection-our-autoencodr.ipynb
```

or

```text
anomaly-detection-pretrained-models.ipynb
```

---

# Machine Learning

The anomaly-detection experiments investigate two main approaches.

## Custom Autoencoder

```text
Input
  │
  ▼
Convolutional Encoder
  │
  ▼
Latent Representation
  │
  ▼
Decoder
  │
  ▼
Reconstructed Input
  │
  ▼
Reconstruction Error
  │
  ▼
Anomaly Score
```

The reconstruction error can be used to identify samples that differ significantly from the normal data.

## Pretrained Models

Pretrained computer-vision models can also be used as feature extractors.

```text
Input Image / Histogram
          │
          ▼
   Pretrained CNN
          │
          ▼
 Feature Embedding
          │
          ▼
 Anomaly Detection
```

---

# Playwright Automation

The repository contains several browser-automation scripts:

```text
playwright_wiki_bot.py
playwright_youtube_bot.py
playwright_soundcloud_bot.py
```

They can be used individually or through `record_scr.py`.

Make sure Playwright and its browser dependencies have been installed:

```powershell
pip install playwright
playwright install
```

---

# Notes

Some scripts expect a particular directory structure and input format. The examples in this README use the `python_for_handin` directory structure:

```text
python_for_handin/
├── data_processing/
├── sts/
├── record_scr.py
├── playwright_wiki_bot.py
└── ...
```

Update the paths in the commands when your local directory structure is different.

---

# Author

**Nachman Rog**

GitHub: https://github.com/nachman1998

