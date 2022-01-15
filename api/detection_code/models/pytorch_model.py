import torch
from langdetect import detect as lang
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
from api.detection_code.models.lstm_attn import LSTMAttentionModel

def detector(text, tokenizer_path, model_path):
    if not lang(text) == "en":
        return "Captions not Engligh!\nUnable to detect..."
    print(lang(text))
    with open(tokenizer_path) as f:
        tokenizer = tokenizer_from_json(f.read())
    print(tokenizer)
    print(len(tokenizer.word_index)+1)
    args = {
        'max_nb_words': len(tokenizer.word_index)+1,
        'max_seq_len': 3000,
        'embedding_dim': 100
    }
    seq = tokenizer.texts_to_sequences([text])
    seq = torch.LongTensor(pad_sequences(seq, maxlen = 3000))
    # print(seq)
    # print(model_path)
    # model = torch.load(model_path)
    model = LSTMAttentionModel(args)
    # print("1", model)
    # print(model_path)
    # print(torch.load(model_path))
    model.load_state_dict(torch.load(model_path))
    # print("2", model)
    model.eval()
    # print("3", model)
    # print(seq.shape)
    det = model(seq)
    print(det)
    return torch.argmax(det, dim=1).tolist()[0]