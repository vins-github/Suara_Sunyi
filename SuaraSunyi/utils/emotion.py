# from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
# import torch
# import torchaudio
# import torchaudio.transforms as T

# # Nama model dari HuggingFace
# model_name = "superb/hubert-large-superb-er"

# # Load model dan feature extractor
# extractor = AutoFeatureExtractor.from_pretrained(model_name)
# model = AutoModelForAudioClassification.from_pretrained(model_name)

# # Mapping label ID ke emosi Bahasa Indonesia
# id2label = {
#     0: "netral",
#     1: "marah",
#     2: "jijik",
#     3: "takut",
#     4: "bahagia",
#     5: "sedih",
#     6: "kagum",
#     7: "lelah"
# }


# def detect_emotion(audio_path):
#     waveform, sample_rate = torchaudio.load(audio_path)

#     # Resample kalau tidak 16000 Hz
#     if sample_rate != 16000:
#         resampler = T.Resample(orig_freq=sample_rate, new_freq=16000)
#         waveform = resampler(waveform)
#         sample_rate = 16000

#     # Convert stereo ke mono (optional, tapi aman)
#     if waveform.shape[0] > 1:
#         waveform = waveform.mean(dim=0, keepdim=True)

#     inputs = extractor(
#         waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt"
#     )

#     with torch.no_grad():
#         logits = model(**inputs).logits

#     predicted_class_id = torch.argmax(logits, dim=1).item()
#     predicted_emotion = id2label[predicted_class_id]

#     return predicted_emotion


from transformers import AutoTokenizer, AutoModelForSequenceClassification, MarianMTModel, MarianTokenizer
import torch

# Load emotion model (English)
emo_model_name = "j-hartmann/emotion-english-distilroberta-base"
emo_tokenizer = AutoTokenizer.from_pretrained(emo_model_name)
emo_model = AutoModelForSequenceClassification.from_pretrained(emo_model_name)

# Load Indonesian-to-English translator
trans_model_name = "Helsinki-NLP/opus-mt-id-en"
trans_tokenizer = MarianTokenizer.from_pretrained(trans_model_name)
trans_model = MarianMTModel.from_pretrained(trans_model_name)

# English -> Indonesian label mapping
eng2indo = {
    "anger": "marah",
    "disgust": "jijik",
    "fear": "takut",
    "joy": "bahagia",
    "neutral": "netral",
    "sadness": "sedih",
    "surprise": "kagum"
}

def detect_emotion(text_id):
    # Terjemahkan ke Inggris
    trans_inputs = trans_tokenizer([text_id], return_tensors="pt", truncation=True)
    trans_outputs = trans_model.generate(**trans_inputs)
    text_en = trans_tokenizer.batch_decode(trans_outputs, skip_special_tokens=True)[0]

    # Deteksi emosi
    inputs = emo_tokenizer(text_en, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = emo_model(**inputs).logits
    predicted_id = torch.argmax(logits, dim=1).item()
    label_eng = emo_model.config.id2label[predicted_id]
    return eng2indo[label_eng]


