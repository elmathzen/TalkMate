import torch
from transformers import pipeline


def summarize_model(text, max_length=100, min_length=30, batch_size=8, top_k=10, top_p=0.4, do_sample=True):  
    # Check if a GPU is available and if not, use a CPU
    device = 0 if torch.cuda.is_available() else -1 

    # Initialize the summarizer
    summarizer = pipeline("summarization", model="Falconsai/text_summarization", device=device, batch_size=batch_size, top_k=top_k, top_p=top_p)
    
    # Split text into chunks 512 tokens (because max tokens for falcon)
    chunks = [text[i:i+512] for i in range(0, len(text), 512)]

    # Summarize each chunk
    summaries = [summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text'] for chunk in chunks]

    # Combine the summaries
    summary = " ".join(summaries)
    return summary
