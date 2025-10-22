
# Structured Chunking Demo (GitHub-ready)

This repository is a starter template demonstrating advanced chunking strategies for structured PDFs (insurance policies, contracts, legal documents).

## What changed from the starter zip
- Added GitHub CI workflow (`.github/workflows/ci.yml`) with a lightweight smoke test.
- Added `.gitignore` and `LICENSE` (MIT).
- Expanded README with instructions to push to GitHub.
- Kept the same `src/` and `notebooks/` but improved docs and examples.

## Quick start (local)
1. Create virtualenv and install minimal deps:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Replace `data/*.pdf` with your real PDFs (do not commit private PDFs to GitHub).
3. Run the pipeline:
   ```bash
   python src/main_pipeline.py --pdf data/sample_policy.pdf
   ```

## How to create a new GitHub repo and push this template
```bash
cd structured_chunking_demo
git init
git add .
git commit -m "Initial commit: structured chunking demo"
gh repo create yourusername/structured-chunking-demo --public --source=. --remote=origin
git push -u origin main
```
(If you don't have `gh` CLI, create the repo on github.com and follow the provided push instructions.)

## CI
The GitHub Actions workflow runs a minimal smoke test to ensure parsing imports work.
You can extend it to run unit tests or notebooks conversion as needed.

## Notes on privacy
- Do **not** commit real client or private legal documents to public repos.
- Use `.gitignore` to exclude `data/*.pdf` from commits.
