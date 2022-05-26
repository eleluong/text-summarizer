from transformers import RobertaModel
from transformers.file_utils import cached_path, hf_bucket_url
from importlib.machinery import SourceFileLoader
import os

cache_dir='./cache'
model_name='nguyenvulebinh/envibert'

def download_tokenizer_files():
  resources = ['envibert_tokenizer.py', 'dict.txt', 'sentencepiece.bpe.model']
  for item in resources:
    if not os.path.exists(os.path.join(cache_dir, item)):
      tmp_file = hf_bucket_url(model_name, filename=item)
      tmp_file = cached_path(tmp_file,cache_dir=cache_dir)
      os.rename(tmp_file, os.path.join(cache_dir, item))
      
download_tokenizer_files()
tokenizer = SourceFileLoader("envibert.tokenizer", os.path.join(cache_dir,'envibert_tokenizer.py')).load_module().RobertaTokenizer(cache_dir)
model = RobertaModel.from_pretrained(model_name,cache_dir=cache_dir)
print("Abc")
