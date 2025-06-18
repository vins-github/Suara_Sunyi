import speech_recognition as sr

def transcribe_audio(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio, language='id-ID')
        except:
            return "[Transkripsi gagal]"
