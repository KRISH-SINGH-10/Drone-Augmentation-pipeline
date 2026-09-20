"""Check local prerequisites without running or fabricating a motion."""
from pathlib import Path
import argparse
import importlib
import sys

from dataset_prep import trumans_paths as paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['ar', 'vq_direct'], default='ar')
    args = parser.parse_args()
    missing = []

    def check(label, ready):
        print(f"{'OK     ' if ready else 'MISSING'} {label}")
        if not ready:
            missing.append(label)

    print(f'Python: {sys.version.split()[0]}')
    for module in ['torch', 'torchvision', 'numpy', 'scipy', 'smplx',
                   'transformers', 'sentencepiece', 'tensorboard', 'aitviewer',
                   'trimesh', 'skvideo', 'yaml', 'matplotlib']:
        try:
            importlib.import_module(module)
            check(f'Package {module}', True)
        except Exception as exc:
            check(f'Package {module}: {exc}', False)

    weights = [('VQ', paths.VQ_WEIGHTS_PATH),
               ('Refinement', paths.REFINEMENT_WEIGHTS_PATH)]
    if args.mode == 'ar':
        weights.append(('AR', paths.AR_WEIGHTS_PATH))
    for name, filename in weights:
        file = Path(filename)
        check(f'{name} weights: {file}', file.is_file())
        options = file.parent.parent / 'opt.txt'
        check(f'{name} options: {options}', options.is_file())

    if args.mode == 'ar':
        try:
            from huggingface_hub import try_to_load_from_cache
            for name in ['config.json', 'model.safetensors', 'spiece.model', 'tokenizer_config.json']:
                cached = try_to_load_from_cache('google/flan-t5-large', name)
                check(f'T5 cached file: {name}', isinstance(cached, str) and Path(cached).is_file())
        except Exception as exc:
            check(f'T5 cache: {exc}', False)

    body = Path(paths.SMPLX_MODEL_DIR) / 'SMPLX_MALE.npz'
    check(f'Licensed SMPL-X male model: {body}', body.is_file())
    prepared = Path(paths.PREPROCESSED_TRUMANS_DIR)
    for name in ['Mean.npy', 'Std.npy']:
        file = prepared / name
        check(f'Normalization: {file}', file.is_file())
    samples = Path(paths.test_samples_path())
    check(f'Test sample list: {samples}', samples.is_file())
    check(f'Prepared motion PKLs: {prepared}', any(prepared.glob('*.pkl')))
    raw = Path(paths.resolve_trumans_data_root())
    check(f'TRUMANS scene arrays: {raw / "Scene"}', any((raw / 'Scene').glob('*.npy')))
    # The upstream loader silently substitutes zeros when features are absent.
    # Reject that condition here rather than claiming proper scene conditioning.
    features = raw / 'Recordings' / 'dinov3' / 'specialized_features_output'
    check(f'DINO scene features: {features}', any(features.glob('*/*/*_unpooled.npy')))

    if missing:
        print(f'\nNot ready: {len(missing)} prerequisite checks failed.')
        print('See LOCAL_SETUP.md. No inference was run.')
        return 1
    print('\nBasic prerequisites found. A successful inference run is still required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
