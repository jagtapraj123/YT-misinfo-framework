from api.detection_code.scraper.caption_scraper import captionScraper
from langdetect import detect as lang
from api.detection_code.models.pytorch_model import detector
import torch.nn as nn
from api.detection_code.models.lstm_attn import LSTMAttentionModel
from api.detection_code.models.lstm import LSTMModel


def detect(videoID, topic):
    captions = captionScraper(videoID)
    print(captions)
    print(captions == None)
    if captions == None:
        return "No captions present for the video."
    elif not lang(captions) == "en":
        return "Captions not in English! Unable to detect..."

    return [
        {
            "model": "LSTM with Attention",
            "value": detector(captions, LSTMAttentionModel, 'api/detection_code/models/saved_models/lstm_attn_{}/tokenizer.json'.format(topic), 'api/detection_code/models/saved_models/lstm_attn_{}/model_state_dict.pth'.format(topic))
        },
        {
            "model": "Bi-LSTM",
            "value": detector(captions, LSTMModel, 'api/detection_code/models/saved_models/lstm_{}/tokenizer.json'.format(topic), 'api/detection_code/models/saved_models/lstm_{}/model_state_dict.pth'.format(topic))
        }
    ]
