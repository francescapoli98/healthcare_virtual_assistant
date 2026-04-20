import os
import json
from datasets import load_dataset

CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache_asclepius.json")


def load_mimic(base_path: str = None):
    """
    VERSIONE SEMPLIFICATA:
    Usa SOLO Asclepius, evitando mimic-iii.
    Si mantengono i nomi delle funzioni per compatibilità nel resto del progetto.
    """
    yield from _load_clinical_qa()


def _load_clinical_qa():
    """
    Caricamento Asclepius con cache locale.
    """

    # usa cache se esiste
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached_data = json.load(f)

            for item in cached_data:
                yield item

            return

        except Exception as e:
            print(f"[Asclepius] Errore cache, ricarico dataset: {e}")

    # carica dataset HF solo se necessario
    try:
        ds = load_dataset(
            "starmpcc/Asclepius-Synthetic-Clinical-Notes",
            split="train",
            token=os.getenv("HF_TOKEN")
        )

        cached_data = []

        for row in ds:
            note = str(row.get("note", "")).strip()
            question = str(row.get("question", "")).strip()
            answer = str(row.get("answer", "")).strip()

            if not note:
                continue

            text = f"Nota clinica:\n{note}"

            if question and answer:
                text += f"\n\nQuesito clinico: {question}\nRisposta: {answer}"

            item = {
                "text": text[:800],
                "source": "asclepius/clinical_notes"
            }

            cached_data.append(item)
            yield item

        # salva cache
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cached_data, f)

            print("[Asclepius] Cache salvata con successo")

        except Exception as e:
            print(f"[Asclepius] Errore salvataggio cache: {e}")

    except Exception as e:
        print(f"[Asclepius] Errore caricamento dataset: {e}")