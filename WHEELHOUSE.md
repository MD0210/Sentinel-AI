# Sentinel AI wheelhouse

The `wheel/` directory is the offline package cache for Sentinel AI's Windows voice environment.

On a machine with internet access, populate it with:

    python -m pip download -r requirements-voice.txt -d wheel

The setup script installs with `--no-index --find-links wheel`, so installation does not contact PyPI.

Wheel binaries are intentionally ignored by Git because they can be large and are platform/Python-version specific.