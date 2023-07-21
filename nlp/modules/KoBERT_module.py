from kobert.pytorch_kobert import get_pytorch_kobert_model
from kobert.utils import get_tokenizer

import torch
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import gluonnlp as nlp

import numpy as np

device = torch.device(
    "cuda:0") if torch.cuda.is_available() else torch.device("cpu")

bertmodel, vocab = get_pytorch_kobert_model()
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)


class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size=768,
                 num_classes=10,
                 dr_rate=0.5,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(
        ), attention_mask=attention_mask.float().to(token_ids.device))
        global out
        out = self.dropout(pooler)
        return self.classifier(out)


class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))


emotion_list = ['Anger', 'malice', 'sad', 'despair', 'dismay', 'worry', 'jealousy', 'hurt', 'love', 'happiness']


def load_nlp_model(PATH='./modules/', model_name='10emotions_model_state_dict_2_10epoch.pt'):
    print('LOADING KOBERT MODEL')
    model = BERTClassifier(bertmodel)
    model.load_state_dict(torch.load(PATH+model_name, map_location='cpu'))
    print('LOADED SUCCESSFULLU')

    return model


def emotion_predict(model, predict_sentence, emotion_list=emotion_list, max_len=128):

    data = [[predict_sentence, '0']]

    another_test = BERTDataset(data, 0, 1, tok, max_len, True, False)
    dataloader = DataLoader(
        another_test, batch_size=64, num_workers=0)

    model.eval()
    for (token_ids, valid_length, segment_ids, label) in dataloader:
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        label = label.long().to(device)

        out = model(token_ids, valid_length, segment_ids)

    result = [0]*10
    for i in range(10):
        result[i] = (emotion_list[i] , round(float(out[0][i]), 3))

    return result
