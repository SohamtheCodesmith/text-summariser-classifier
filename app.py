import gradio as gr
from models.summariser import summarise, SUMMARISATION_MODELS
from models.classifier import classify, CLASSIFIER_MODELS

def estimate_tokens(text):
    return int(len(text.split()) * 1.5)

def run_summarisation(text, model_name, max_len):
    try:
        if not text.strip():
            return "ERROR: Input text is empty!"

        token_estimate = estimate_tokens(text)
        warning = ""
        if token_estimate > 512:
            warning = "WARNING: Input likely exceeds model limit, and will be truncated.\n\n"

        summary = summarise(text, model_name, max_len=max_len, min_len=int(max_len * 0.5))
        return warning + summary

    except Exception as e:
        return f"SUMMARISATION ERROR: {str(e)}"

def run_classification(text, model_name, labels_str):
    try:
        if not text.strip():
            return "ERROR: Input text is empty!"
        labels = [lbl.strip() for lbl in labels_str.split(",") if lbl.strip()]
        if not labels:
            return "ERROR: No valid labels provided!"

        classes, scores = classify(text, model_name, labels)
        result = "| Label | Score |\n|-------|-------|\n" + "\n".join([f"| {label} | {score:.2f} |" for label, score in zip(classes, scores)])
        return result
    except Exception as e:
        return f"CLASSIFICATION ERROR: {str(e)}"

model_names_sum = list(SUMMARISATION_MODELS.keys())
model_names_cla = list(CLASSIFIER_MODELS.keys())


with gr.Blocks() as liveDemo:
    with gr.Tab("Summariser"):
        gr.Markdown("### Text Summarisation")
        input_text = gr.Textbox(lines=10, max_lines=10, label="Input Text")
        model_selector = gr.Dropdown(choices=model_names_sum, value=model_names_sum[0], label="Model")
        maxlen_slider = gr.Slider(50, 512, value=120, step=10, label="Max Length")
        output_summary = gr.Textbox(label="Summary Output", max_lines=5)
        summarise_btn = gr.Button("Summarise")
        summarise_btn.click(run_summarisation, [input_text, model_selector, maxlen_slider], output_summary)

    with gr.Tab("Classifier"):
        gr.Markdown("### Text Classification (Zero-Shot)")
        classify_text = gr.Textbox(lines=10, max_lines=10, label="Text to Classify")
        model_selector = gr.Dropdown(choices=model_names_cla, value=model_names_cla[0], label="Model")
        labels_input = gr.Textbox(label="Candidate Labels (Separated by Commas)")
        output_classes = gr.Markdown(container=True, min_height=100)
        classify_btn = gr.Button("Classify")
        classify_btn.click(run_classification, [classify_text, model_selector, labels_input], output_classes)

if __name__ == "__main__":
    liveDemo.launch()