import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.nn import functional as F
import numpy as np

class LSTMAttentionModel(nn.Module):
    def __init__(self, args):
        super(LSTMAttentionModel, self).__init__()

        # self.batch_size = batch_size
        # self.output_size = output_size
        # self.hidden_size = hidden_size
        # self.vocab_size = vocab_size
        # self.embedding_length = embedding_length

        # self.word_embeddings = nn.Embedding(vocab_size, embedding_length)
        # self.word_embeddings.weights = nn.Parameter(weights, requires_grad=False)
        

        self.embedding_dim = args['embedding_dim']
        self.max_nb_words = args['max_nb_words']

        if args.get('pretrained_embeds') is not None:
            self.embed = nn.Embedding.from_pretrained(torch.Tensor(args.get('pretrained_embeds')), args.get('freeze_embeds') == True)
        else:
            self.embed = nn.Embedding(self.max_nb_words, self.embedding_dim)

        self.lstm = nn.LSTM(input_size=self.embedding_dim, hidden_size=64, num_layers=1, batch_first=True, bidirectional=False)
        self.label = nn.Linear(64, 3)
        #self.attn_fc_layer = nn.Linear()

    def attention_net(self, lstm_output, final_state):
        hidden = final_state.squeeze(0)
        # print(hidden.shape, hidden.unsqueeze(2).shape)
        attn_weights = torch.bmm(lstm_output, hidden.unsqueeze(2)).squeeze(2)
        soft_attn_weights = F.softmax(attn_weights, 1)
        new_hidden_state = torch.bmm(lstm_output.transpose(1, 2), soft_attn_weights.unsqueeze(2)).squeeze(2)
        print(soft_attn_weights.shape)
        print(new_hidden_state.shape)
        return new_hidden_state, soft_attn_weights

    def forward(self, input_sentences):
        input = self.embed(input_sentences)
        # input = input.permute(1, 0, 2)
        # print(input.shape)
        output, (final_hidden_state, final_cell_state) = self.lstm(input) # final_hidden_state.size() = (1, batch_size, hidden_size) 
        # output = output.permute(1, 0, 2) # output.size() = (batch_size, num_seq, hidden_size)
        # print(output.shape, final_hidden_state.shape, final_cell_state.shape)

        attn_output, attention = self.attention_net(output, final_hidden_state)
        logits = self.label(attn_output)

        return logits, attention

    # def get_attention(self, input_sentences):
    #     input = self.embed(input_sentences)
    #     # input = input.permute(1, 0, 2)
    #     # print(input.shape)
    #     output, (final_hidden_state, final_cell_state) = self.lstm(input) # final_hidden_state.size() = (1, batch_size, hidden_size) 
    #     # output = output.permute(1, 0, 2) # output.size() = (batch_size, num_seq, hidden_size)
    #     # print(output.shape, final_hidden_state.shape, final_cell_state.shape)

    #     hidden = final_hidden_state.squeeze(0)
    #     # print(hidden.shape, hidden.unsqueeze(2).shape)
    #     attn_weights = torch.bmm(output, hidden.unsqueeze(2)).squeeze(2)
    #     soft_attn_weights = F.softmax(attn_weights, 1)
    #     print(soft_attn_weights.shape)
    #     return soft_attn_weights