import torch

REPO_OR_DIR = 'snakers4/silero-models'
MODEL = 'silero_tts'

# silero - text to voice
LANGUAGE = 'ru'
MODEL_ID = 'ru_v3'
SAMPLE_RATE = 48000
SPEAKER = 'xenia'  # aidar, baya, kseniya, xenia, random
PUT_ACCENT = True
PUT_YO = True
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model, _ = torch.hub.load(repo_or_dir=REPO_OR_DIR, model=MODEL,
                          language=LANGUAGE, speaker=MODEL_ID)
model.to(device)


def text_to_speech(text, speak=SPEAKER, path='audio/result.wav'):
    audio = model.save_wav(text=text,
                           speaker=speak,
                           sample_rate=SAMPLE_RATE,
                           put_accent=PUT_ACCENT,
                           put_yo=PUT_YO,
                           audio_path=path)
    return audio
