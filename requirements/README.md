# Optional Requirement Groups

`../requirements.txt` is the base runtime for the existing corpus pipeline.

These files document endpoint-specific optional stacks. Install them only for the track that needs them.
`requirements.txt` in this directory is an aggregate manifest for GitHub Dependency Graph visibility; it is not the default runtime install target.

```powershell
python -m pip install -r requirements\xml.txt
python -m pip install -r requirements\rdf.txt
python -m pip install -r requirements\nlp.txt
```

The optional groups intentionally do not include large model downloads. Track implementations must record model names, versions, and download commands in their validation manifests.
