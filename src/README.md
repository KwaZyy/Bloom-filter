This folder no longer contains the main Bloom filter implementation.

The canonical implementation for this project is in `bloomfilter/`.

Why this note exists:
- An older duplicate implementation used to live in `src/`.
- Keeping two versions of the Bloom filter in the repository can confuse readers and graders.
- The maintained version is now the package in `bloomfilter/`.

Use these files instead:
- `bloomfilter/bloom.py` for the Bloom filter implementation
- `bloomfilter/__init__.py` for the package interface
- `bloomfilter/__main__.py` for the command-line entry point
