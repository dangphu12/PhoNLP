# -*- coding: utf-8 -*-
import torch
from phonlp.annotate_model import JointModel
from phonlp.models.ner.vocab import MultiVocab
from phonlp.models.common import utils as util
from transformers import AutoConfig, AutoTokenizer
import gdown



def download(save_dir, url="https://drive.google.com/uc?id=1ix2Yse5SnTIWSnANluCHemdYmZtkUQN6"):
    util.ensure_dir(save_dir)
    if save_dir[len(save_dir) - 1] == '/':
        model_file = save_dir + "phonlp.pt"
    else:
        model_file = save_dir + "/phonlp.pt"
    gdown.download(url, model_file)

def load(save_dir='./'):
    if save_dir[len(save_dir) - 1] == '/':
        model_file = save_dir + "phonlp.pt"
    else:
        model_file = save_dir + "/phonlp.pt"
    tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base', use_fast=False)
    config_phobert = AutoConfig.from_pretrained('vinai/phobert-base', output_hidden_states=True)
    print("Loading model from: {}".format(model_file))
    checkpoint = torch.load(model_file, lambda storage, loc: storage)
    args = checkpoint['config']
    vocab = MultiVocab.load_state_dict(checkpoint['vocab'])
    # load model
    model = JointModel(args, vocab, config_phobert, tokenizer)
    model.load_state_dict(checkpoint['model'], strict=False)
    if torch.cuda.is_available() == False:
        model.to(torch.device('cpu'))
    else:
        model.to(torch.device('cuda'))
    model.eval()
    return model

if __name__ == '__main__':
    download("./")
    model = load("./")
    text = "Tôi tên là Thế_Linh ."
    output = model.annotate(text=text)
    model.print_out(output)

