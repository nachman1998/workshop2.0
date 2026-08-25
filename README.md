# Workshop 2.0

A comprehensive collection of machine learning notebooks and automation scripts for anomaly detection using autoencoders, web scraping, and media processing.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Notebooks](#notebooks)
- [Scripts](#scripts)
- [Requirements](#requirements)
- [Getting Started](#getting-started)

## Overview

This repository is a workshop project containing:

- **Machine Learning**: Deep learning-based autoencoder models for anomaly detection
- **Web Automation**: Playwright-based bots for scraping and interacting with platforms (YouTube, SoundCloud, Wikipedia)
- **Media Tools**: Utilities for screen recording and image visualization

**Language Composition:**
- Jupyter Notebooks: 88.8%
- Python: 11.2%

## Project Structure

```
workshop2.0/
├── README.md                              # This file
├── autoencoder-model-build.ipynb          # Build and train autoencoder models
├── anomaly-detection-our-autoencodr.ipynb # Custom autoencoder anomaly detection
├── anomaly-detection-pretrained-models.ipynb # Pretrained model anomaly detection
├── playwright_youtube_bot.py               # YouTube web automation bot
├── playwright_soundcloud_bot.py            # SoundCloud web automation bot
├── playwright_wiki_bot.py                  # Wikipedia web automation bot
├── pics_view.py                            # Image visualization utility
├── record_scr.py                           # Screen recording utility
└── data_processing/                        # Data preprocessing modules
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda
- Jupyter Notebook or JupyterLab (for notebooks)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/nachman1998/workshop2.0.git
   cd workshop2.0
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (for web automation scripts)
   ```bash
   playwright install
   ```

5. **Launch Jupyter** (for notebooks)
   ```bash
   jupyter notebook
   ```

## Usage

### Notebooks

#### 1. Autoencoder Model Build
**File:** `autoencoder-model-build.ipynb`

Build and train autoencoder neural networks from scratch.

```bash
jupyter notebook autoencoder-model-build.ipynb
```

**What you'll learn:**
- Autoencoder architecture and design
- Model training and optimization
- Parameter tuning and experimentation

---

#### 2. Custom Autoencoder Anomaly Detection
**File:** `anomaly-detection-our-autoencodr.ipynb`

Use your trained autoencoder to detect anomalies in data.

```bash
jupyter notebook anomaly-detection-our-autoencodr.ipynb
```

**Features:**
- Reconstruction error calculation
- Anomaly threshold determination
- Visualization of anomalies

---

#### 3. Pretrained Models Anomaly Detection
**File:** `anomaly-detection-pretrained-models.ipynb`

Leverage pretrained models for quick anomaly detection without training.

```bash
jupyter notebook anomaly-detection-pretrained-models.ipynb
```

**Capabilities:**
- Load and use pretrained models
- Compare different architectures
- Fine-tune on custom data

### Scripts

#### YouTube Bot
**File:** `playwright_youtube_bot.py`

Automate YouTube interactions and data collection.

```bash
python playwright_youtube_bot.py
```

**Uses:**
- Video metadata scraping
- Channel automation
- Playlist management

---

#### SoundCloud Bot
**File:** `playwright_soundcloud_bot.py`

Interact with SoundCloud for data collection or testing.

```bash
python playwright_soundcloud_bot.py
```

**Features:**
- Track information extraction
- User profile automation
- Playlist operations

---

#### Wikipedia Bot
**File:** `playwright_wiki_bot.py`

Automate Wikipedia navigation and data extraction.

```bash
python playwright_wiki_bot.py
```

**Capabilities:**
- Page content scraping
- Link traversal
- Information extraction

---

#### Screen Recording
**File:** `record_scr.py`

Record screen activity to create demonstrations or tutorials.

```bash
python record_scr.py
```

**Options:**
- Customizable recording resolution
- Audio capture
- Video format selection

---

#### Image Visualization
**File:** `pics_view.py`

Display and analyze images interactively.

```bash
python pics_view.py
```

**Uses:**
- Anomaly detection results visualization
- Image comparison
- Dataset exploration

## Notebooks

### Key Notebooks Overview

| Notebook | Purpose | Level |
|----------|---------|-------|
| `autoencoder-model-build.ipynb` | Build neural network autoencoders | Intermediate |
| `anomaly-detection-our-autoencodr.ipynb` | Apply custom autoencoders for anomaly detection | Advanced |
| `anomaly-detection-pretrained-models.ipynb` | Use pretrained models for quick implementation | Beginner |

## Scripts

### Key Scripts Overview

| Script | Purpose | Language |
|--------|---------|----------|
| `playwright_youtube_bot.py` | YouTube automation | Python |
| `playwright_soundcloud_bot.py` | SoundCloud automation | Python |
| `playwright_wiki_bot.py` | Wikipedia automation | Python |
| `pics_view.py` | Image visualization | Python |
| `record_scr.py` | Screen recording | Python |

## Requirements

### Core Dependencies

```
jupyter>=1.0.0
pandas>=1.0.0
numpy>=1.19.0
matplotlib>=3.0.0
scikit-learn>=0.24.0
tensorflow>=2.0.0
keras>=2.4.0
```

### Web Automation

```
playwright>=1.30.0
```

### Media Processing

```
opencv-python>=4.5.0
```

### Utility Libraries

```
Pillow>=8.0.0
scipy>=1.5.0
```

## Getting Started

### For Machine Learning Beginners:
1. Start with `anomaly-detection-pretrained-models.ipynb`
2. Understand the basics of anomaly detection
3. Progress to custom model building

### For Web Scraping:
1. Review the relevant bot script (YouTube/SoundCloud/Wikipedia)
2. Update selectors if needed (websites may change structure)
3. Run in headless mode for background execution

### For Full Understanding:
1. Study `autoencoder-model-build.ipynb` for architecture
2. Explore `anomaly-detection-our-autoencodr.ipynb` for applications
3. Try `anomaly-detection-pretrained-models.ipynb` for quick implementation
4. Experiment with web automation scripts

## Important Notes

⚠️ **Web Scraping Disclaimer:**
- Ensure you have proper permissions before scraping any website
- Check the website's `robots.txt` and terms of service
- Use respectful scraping practices (delays, user agents)
- Web bots may require updates if target sites change their structure

💡 **Performance Tips:**
- Use GPU acceleration for machine learning notebooks (requires CUDA/cuDNN)
- For large datasets, consider data sampling before full processing
- Run web bots during off-peak hours for better performance

🔧 **Troubleshooting:**
- If Playwright fails, reinstall browsers: `playwright install`
- If models won't load, verify TensorFlow/Keras versions match
- For notebook issues, try restarting the kernel and clearing outputs

## License

This project is public. See LICENSE file for details (if available).

## Contributing

Contributions are welcome! Feel free to:
- Submit bug reports and feature requests
- Create pull requests with improvements
- Share your results and applications

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Created:** August 2026  
**Repository:** [nachman1998/workshop2.0](https://github.com/nachman1998/workshop2.0)
