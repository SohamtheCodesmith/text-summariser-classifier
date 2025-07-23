from transformers import pipeline

# Preloading the supported models

SUMMARISATION_MODELS = {
    "BART (facebook/bart-large-cnn)": "facebook/bart-large-cnn",
    "T5 Base (t5-base)": "t5-base",
    "T5 Small (t5-small)": "t5-small",
    "DistilBART (sshleifer/distilbart-cnn-12-6)": "sshleifer/distilbart-cnn-12-6",
    "Pegasus News (google/pegasus-cnn_dailymail)": "google/pegasus-cnn_dailymail",
    "LongT5 (google/long-t5-tglobal-base)": "google/long-t5-tglobal-base",
}

_loaded_summarisers = {}

def get_summariser(model_name: str):
    if model_name not in _loaded_summarisers:
        hf_model_id = SUMMARISATION_MODELS[model_name]
        _loaded_summarisers[model_name] = pipeline("summarization", model=hf_model_id)
    return _loaded_summarisers[model_name]

def summarise(text: str, model_name: str, max_len=100, min_len=30):
    summariser = get_summariser(model_name)
    summary = summariser(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]["summary_text"]