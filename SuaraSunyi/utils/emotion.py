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


