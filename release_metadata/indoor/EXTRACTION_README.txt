Indoor_condition_dataset: two independent ZIP archives

Download BOTH ZIP files and extract BOTH into the SAME parent directory.
Both archives contain the common top-level folder Indoor_condition_dataset/.
Their contents are complementary, so extracting them together restores the full dataset.
These are independent ZIP archives, not .z01/.z02 split volumes.

part01_train.zip:
  images/train/, labels/train/, and the root metadata/configuration/README files.

part02_val_test.zip:
  images/val/, images/test/, labels/val/, labels/test/, test_slices/,
  plus any other non-training support files present in the original folder.

Example on Windows PowerShell, from the directory containing both archives:
  Expand-Archive -LiteralPath .\Indoor_condition_dataset_part01_train.zip -DestinationPath .\extracted
  Expand-Archive -LiteralPath .\Indoor_condition_dataset_part02_val_test.zip -DestinationPath .\extracted

Example on Linux/macOS:
  unzip Indoor_condition_dataset_part01_train.zip -d extracted
  unzip Indoor_condition_dataset_part02_val_test.zip -d extracted

Check download hashes against SHA256SUMS.txt:
  PowerShell: Get-FileHash -Algorithm SHA256 .\Indoor_condition_dataset_part*.zip
  Linux:     sha256sum -c SHA256SUMS.txt

Every original file is included without content changes, including existing cache files.
Every archived file was decoded and checked against its source SHA-256 hash.
dataset_manifest.csv records original relative paths, file sizes, hashes and archive membership.
Both ZIP files are strictly below 2,000,000,000 bytes (decimal 2 GB).

Original data.yaml and test_slices paths have been preserved as supplied.
They may refer to a previous workstation; update configuration paths for your environment.
