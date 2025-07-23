from transformers import pipeline

# Preloading the supported models

CLASSIFIER_MODELS = {
    "BART MNLI (facebook/bart-large-mnli)": "facebook/bart-large-mnli",
    "RoBERTa MNLI (roberta-large-mnli)": "roberta-large-mnli",
    "DeBERTa (microsoft/deberta-large-mnli)": "microsoft/deberta-large-mnli"
}

_loaded_classes = {}

def get_classifier(model_name: str):
    if model_name not in _loaded_classes:
        hf_model_id = CLASSIFIER_MODELS[model_name]
        _loaded_classes[model_name] = pipeline("zero-shot-classification", model=hf_model_id)
    return _loaded_classes[model_name]

def classify(text: str, model_name: str, candidate_labels):
    classifier = get_classifier(model_name)
    result = classifier(text, candidate_labels)
    return result["labels"], result["scores"]