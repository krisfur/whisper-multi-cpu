# Automated PyPI Releases

This repository is set up for automated PyPI releases using GitHub Actions. When you push a tag starting with `v` (e.g., `v1.0.2`), it will automatically:

1. Build the package
2. Upload to PyPI
3. Create a GitHub release with the built artifacts

## Setup

### 1. Create a PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll down to "API tokens"
3. Click "Add API token"
4. Give it a name like "GitHub Actions"
5. Set scope to "Entire account (all projects)"
6. Copy the token (it starts with `pypi-`)

### 2. Add the Token to GitHub Secrets

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI API token

## Making a Release

To create a new release:

1. Update the version in `pyproject.toml`:
   ```toml
   [project]
   version = "1.0.2"
   ```

2. Commit and push the version change:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 1.0.2"
   git push origin main
   ```

3. Create and push a tag:
   ```bash
   git tag -a v1.0.2 -m "Release v1.0.2"
   git push origin v1.0.2
   ```

4. The GitHub Action will automatically:
   - Build the package
   - Upload to PyPI
   - Create a GitHub release

## Manual Release (if needed)

If you need to release manually:

```bash
# Build the package
python -m build

# Upload to PyPI (requires twine)
pip install twine
twine upload dist/*
```

## Troubleshooting

- Check the GitHub Actions tab to see if the workflow ran successfully
- If the workflow fails, check the logs for build errors
- Make sure the PyPI API token has the correct permissions
- Ensure the version in `pyproject.toml` matches the git tag 