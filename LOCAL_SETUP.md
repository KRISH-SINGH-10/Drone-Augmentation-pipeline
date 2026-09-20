# Local SceMoS setup

**Superseded for V1:** use `D:\IITB_L3\Run-V1.ps1` and `D:\IITB_L3\v1\README.md`.
The dataset-based steps below are historical. The large download worker is disabled.
V1 does not use TRUMANS recordings or DINOv3; do not follow the old download steps.

This is the official SceMoS example, not the requested interactive A-to-B application.
Full inference has not yet been validated. Licensed assets and prepared data are missing.
No training, fine-tuning, or trajectory approximation has been added.

## Installed environment

- Project-local Python 3.10.20 and `.venv`.
- PyTorch 2.5.1 CPU and torchvision 0.20.1 CPU. The available GT 1030 has only 2 GB VRAM.
- Dependencies listed in `requirements-local.txt`; exact installed versions in `requirements-local-lock.txt`.
- These version pins are local compatibility choices, not an official SceMoS lockfile.
- `dataset_prep/trumans_paths.py` now uses project-relative paths.
- DINOv3 source is in `dino_feats_extraction/dinov3`; matching pretrained weights require access.

## Commands

In PowerShell:

```powershell
cd D:\IITB_L3
.\Run-SceMoS.ps1 check
```

This prints missing prerequisites and exits unsuccessfully when assets are missing.
It does not generate substitute data or claim that installation means inference works.

After all assets are supplied and preprocessing is complete:

```powershell
.\Run-SceMoS.ps1 reconstruct
.\Run-SceMoS.ps1 generate
.\Run-SceMoS.ps1 view
```

`reconstruct` calls official `vq_direct` on an existing dataset motion.
`generate` calls official `ar` on a dataset sample's text and scene.
Both save native PKLs under `outputs/scemos_infer/test`. Neither accepts a target endpoint.
The upstream loader preloads the split even with `--num_samples 1`, so RAM usage still
depends on the prepared dataset. The launcher defaults to CPU; speed and full-run memory
requirements have not been measured on this machine.

## Public downloads

The resumable worker is `D:\IITB_L3\download_public_assets.py`.
Check `D:\IITB_L3\downloads\status.json` and `public-downloads.log` for its actual state.
Run `D:\IITB_L3\Download-Status.ps1` for current archive byte counts.
Archives are not usable until verified against the official size and MD5 checksum.
The worker downloads/extracts the 2.35 GB checkpoint archive, caches the T5 model,
then downloads/extracts the 11.54 GB BEV archive. Partial archives are preserved on failure.
If the worker has stopped, resume with:

```powershell
cd D:\IITB_L3
.\SceMoS_codebase\.venv\Scripts\python.exe .\download_public_assets.py
```

Do not launch a second worker while one is running.

## Access that you must obtain

1. [SMPL-X registration/download](https://smpl-x.is.tue.mpg.de/): accept the applicable
   terms using your own account. Place the male NPZ model at
   `D:\IITB_L3\SceMoS_codebase\models\smplx\SMPLX_MALE.npz`.
2. [TRUMANS request form](https://docs.google.com/forms/d/e/1FAIpQLSdF62BQ9TQTSTW0HzyNeRPhlzmREL5T8hUGn-484W1I3eVihQ/viewform):
   provide your researcher details and agree to the terms. Put the approved raw release in
   `D:\IITB_L3\SceMoS_codebase\data\TRUMANS\Data_release`.
3. [DINOv3 official pretrained models](https://github.com/facebookresearch/dinov3#pretrained-models):
   request the ConvNeXt-Tiny LVD-1689M weights used by SceMoS, unless matching precomputed
   features are supplied. Do not substitute DINOv2 features for this pretrained checkpoint.

After access, preprocessing and feature extraction still need to be run and tested.
The upstream preprocessing script has its own hardcoded raw-data path that must be
configured then. The current extractor also needs compatibility verification with the
downloaded DINOv3 source. Do not run the README's training stages.

Prepared files expected under `data/trumans`: motion PKLs, `Mean.npy`, `Std.npy`, and
`test_samples.npy` (or legacy `validation_samples.npy`). Normalization must match the
pretrained model; arbitrary statistics or dummy motions are not replacements.
The launcher rejects absent DINO features rather than allowing the upstream loader's
silent zero-feature fallback.

## Scope limitation

The released inference pipeline has no explicit start/end goal conditioning. An
interactive A-to-B application requires a separately agreed adaptation or another model.
Completing this setup only enables the official dataset-based example.

## Checks completed on 2026-09-19

- All 82 installed packages passed `uv pip check`.
- Official inference `--help` executed successfully.
- Official visualization module imported successfully; GUI playback is untested.
- A CPU tensor operation completed successfully.
- The real VQ checkpoint and its options were extracted from the already-downloaded
  archive prefix with ZIP CRC verification. The official `load_vq` loaded its 24,112,393
  parameters successfully on CPU. This was a model-loading test, not motion generation.
- The launcher reports missing licensed assets and prepared data with a nonzero exit.
- Public archive downloads are incomplete until the worker records completion.
