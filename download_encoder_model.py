import wget
import os
from pathlib import Path
import zipfile

root_dir = os.path.dirname(os.path.realpath(__file__))
print(root_dir)

model_dir = Path(root_dir + "/.trained_models")
if not model_dir.is_dir():
  print("Created trained models dir (.trained_models)")
  os.mkdir(model_dir)

encoder_dir = model_dir / "frankie_encoder"
if not encoder_dir.is_dir():
  print("Frankie Encoder does not exist. Will download it.")

  file_name = 'frankie_encoder.zip'
  #file_name = 'test_dir.zip'
  url = 'https://storage.googleapis.com/frankie-training/' + file_name
  wget.download(url, str(model_dir))
  
  frankie_encoder_zip = model_dir / file_name
  
  with zipfile.ZipFile(frankie_encoder_zip, 'r') as zip_ref:
      zip_ref.extractall(model_dir)
  
  extr_zip_dir = model_dir / ".trained_models" / "frankie_encoder"
  extr_zip_dir.rename(model_dir / "frankie_encoder")
  old_dir = model_dir / ".trained_models"
  old_dir.rmdir()

  # Remove zip file after extraction
  frankie_encoder_zip.unlink()