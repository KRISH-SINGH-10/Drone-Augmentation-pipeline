# Layer 3 (IIT Bombay): Scene-Aware Human Motion, early setup

Early work for Layer 3 of the IIT Bombay synthetic drone-data pipeline: generating realistic human motion inside 3D scenes. This repo holds a local setup of the official **SceMoS** (Scene-Aware Motion Synthesis) codebase: data preparation, the motion VQ-VAE and autoregressive model code, evaluation scripts and SMPL-X utilities.

**This version is superseded.** The working pipeline, with multiple SMPL-X actors walking collision-free routes inside 3D Gaussian Splatting digital twins and rendered drone-view video, is in **[Layer3-IITB-V1](https://github.com/KRISH-SINGH-10/Layer3-IITB-V1)**.

## Layout

| Folder | What it holds |
|---|---|
| `dataset_prep/` | Motion preprocessing, height maps, train/test split |
| `train/` | Motion VQ-VAE and autoregressive model training scripts (from SceMoS) |
| `eval/` | Inference pipeline and metrics |
| `dino_feats_extraction/` | Scene feature extraction |
| `common/`, `utils/` | Skeleton, quaternion and SMPL-X helpers |
| `visualize/` | Data visualisation |

Setup notes: [LOCAL_SETUP.md](LOCAL_SETUP.md). Running it needs licensed assets (SMPL-X models and the TRUMANS dataset) that are not included here.

## Credit

Model and training code come from the official SceMoS release; licensed assets belong to their owners. This repo is my local setup and adaptation for the IIT Bombay project.

Author: Krish Singh
