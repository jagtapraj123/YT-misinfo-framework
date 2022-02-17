import torch
from langdetect import detect as lang
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
from api.detection_code.models.lstm_attn import LSTMAttentionModel

STOPWORDS = set([ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", 
    "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during",
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into",
    "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", 
    "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's",
    "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've",
    "your", "yours", "yourself", "yourselves" ])

def detector(text, model: torch.nn.Module, tokenizer_path, model_dict_path):
    if not lang(text) == "en":
        return "Captions not Engligh!\nUnable to detect..."
    print(lang(text))
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
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
    model = model(args)
    # print("1", model)
    # print(model_path)
    # print(torch.load(model_path))
    model.load_state_dict(torch.load(model_dict_path))
    # print("2", model)
    model.eval()
    # print("3", model)
    # print(seq.shape)
    det = model(seq)
    print(det)
    return torch.argmax(det, dim=1).tolist()[0]-1