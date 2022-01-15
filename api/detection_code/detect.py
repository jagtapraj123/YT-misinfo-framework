from api.detection_code.scraper import captionScraper
from api.detection_code.models.pytorch_model import detector
import torch.nn as nn

def detect(videoURL, topic):
    print(videoURL)
    # https://www.youtube.com/watch?v=eXBDPPseOXI
    videoID = videoURL.split('?v=')[1].split('&')[0]
    captions = captionScraper(videoID)
    print(captions)
    # print(detector(captions, 'api/detection_code/models/saved_models/lstm_attn_911/tokenizer.json', 'api/detection_code/models/saved_models/lstm_attn_911/model_state_dict.pth'))
    # return captions
    detection = detector(captions, 'api/detection_code/models/saved_models/lstm_attn_{}/tokenizer.json'.format(topic), 'api/detection_code/models/saved_models/lstm_attn_{}/model_state_dict.pth'.format(topic))
    print(detection)
    return detection-1
    return "Neutral" if detection == 1 else "Misinformation" if detection == 2 else "Debunking Misinformation"