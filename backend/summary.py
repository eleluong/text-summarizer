from importlib.machinery import SourceFileLoader
from transformers import RobertaModel
import os
import re
from sklearn.cluster import KMeans
import numpy as np
from numpy import ndarray
from tqdm import tqdm


cache_dir='./cache'
model_name='nguyenvulebinh/envibert'

tokenizer = SourceFileLoader("envibert.tokenizer", os.path.join(cache_dir,'envibert_tokenizer.py')).load_module().RobertaTokenizer(cache_dir)
model = RobertaModel.from_pretrained(model_name,cache_dir=cache_dir)


class summarizer():
    def __init__(self):
        self.model = model
        self.tokenizer = tokenizer

    def summarize(self, input):
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', input)
        features = self.create_matrix(sentences)
        args = self.cluster(features)
        s = ""
        for j in args:
            s = s + sentences[j] +". "
        return s
        
    def cluster(self, features):
        cluster = KMeans(n_clusters=max(3, len(features)//10)) 
        cluster.fit(features)
        centroids = cluster.cluster_centers_

        centroid_min = 1e7
        cur_arg = -1
        args = {}
        used_idx = []

        for j, centroid in enumerate(centroids):
            for i, feature in enumerate(features):
                value = np.sum(np.abs(feature - centroid))
                if value < centroid_min and i not in used_idx:
                    cur_arg = i
                    centroid_min= value
            used_idx.append(cur_arg)
            args[j] = cur_arg
            centroid_min = 1e7
            cur_arg = -1
        return args

    def tokenize_input(self, text):
        input_ids = self.tokenizer(text, return_tensors = 'pt').input_ids
        return input_ids

    def exact_embedding(self, text) -> ndarray:
        input = self.tokenize_input(text)
        output = self.model(input)
        return output.hidden_states[0].mean(dim = 1)

    def create_matrix(self, content) -> ndarray:
        train_vec = np.zeros((len(content), 768))
        for i, text in tqdm(enumerate(content)):
            train_vec[i]= self.exact_embedding(text).data.numpy()
        return train_vec

