from datasets import load_dataset

def load_medquad():
    dataset = load_dataset("lavita/MedQuAD")

    for item in dataset["train"]:
        q = item.get("question", "")
        a = item.get("answer", "")

        if q and a:
            yield {
                "text": f"Q: {q}\nA: {a}",
                "source": "medquad"
            }