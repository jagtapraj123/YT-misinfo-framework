# https://towardsdatascience.com/text-classification-with-pytorch-7111dae111a6
# https://towardsdatascience.com/implementation-differences-in-lstm-layers-tensorflow-vs-pytorch-77a31d742f74
# https://towardsdatascience.com/lstms-in-pytorch-528b0440244
import torch
import torch.nn as nn
import torch.nn.functional as F

class LSTMModel(nn.Module):
    def __init__(self, args):
        super(LSTMModel, self).__init__()

        self.embedding_dim = args['embedding_dim']
        self.max_nb_words = args['max_nb_words']

        if args.get('pretrained_embeds') is not None:
            self.embed = nn.Embedding.from_pretrained(torch.Tensor(args.get('pretrained_embeds')), args.get('freeze_embeds') == True)
        else:
            self.embed = nn.Embedding(self.max_nb_words, self.embedding_dim)
            
        self.lstm = nn.LSTM(input_size=self.embedding_dim, hidden_size=64, num_layers=2, batch_first=True, bidirectional=True)

        self.classifier = nn.Sequential(
            # nn.Dropout(0.3),
            # nn.Linear(128, 32),
            # nn.ReLU(),
            # nn.Linear(32, 8),
            # nn.ReLU(),
            nn.Linear(128, 3),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        # preds = self.model(x)
        # print(x.shape)
        out = self.embed(x)
        # print(out.shape)
        out, _ = self.lstm(out)
        # print(out.shape, out.reshape(x.shape[0], -1).shape)
        # preds = self.classifier(out.reshape(x.shape[0], -1))
        # print(out[:,-1,:].shape)
        preds = self.classifier(out[:,-1,:])
        # preds = self.classifier(out)
        return preds

