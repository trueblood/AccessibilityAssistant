from datasets import load_dataset
from txtai.pipeline import HFTrainer

ds = load_dataset("squad")

trainer = HFTrainer()

trainer("distilbert-base-uncased", ds["train"].select(range(3000)), task="question-answering", output_dir="distilbert-base-uncased")
