import os
import pandas as pd
from datasets import load_dataset


def load_mimic(base_path: str = None):
    """
    Sostituto di MIMIC-III basato su medical_meadow_clinicalqa.
    Contiene casi clinici reali in formato narrativo — stile simile
    alle discharge summaries di MIMIC (anamnesi, diagnosi, piano).

    Se base_path punta a una cartella con MIMIC demo, carica anche
    quelli come fallback aggiuntivo.
    """
    yield from _load_clinical_qa()

    # Fallback: se hai ancora il demo, lo usa in aggiunta
    if base_path:
        yield from _load_mimic_demo_fallback(base_path)


def _load_clinical_qa():
    try:
        from datasets import load_dataset

        # Asclepius: note cliniche sintetiche stile MIMIC
        # starmpcc/Asclepius-Synthetic-Clinical-Notes
        ds = load_dataset(
            "starmpcc/Asclepius-Synthetic-Clinical-Notes",
            split="train"
        )

        for row in ds:
            note = str(row.get("note", "")).strip()
            question = str(row.get("question", "")).strip()
            answer = str(row.get("answer", "")).strip()

            if not note:
                continue

            # Costruisce testo stile discharge summary
            text = f"Nota clinica:\n{note}"
            if question and answer:
                text += f"\n\nQuesito clinico: {question}\nRisposta: {answer}"

            yield {"text": text[:800], "source": "asclepius/clinical_notes"}

    except Exception as e:
        print(f"[mimic_loader] Errore caricamento Asclepius: {e}")


def _load_mimic_demo_fallback(base_path: str):
    """
    Carica i dati strutturati dal MIMIC-III demo che hai già.
    Estrae diagnosi e procedure come testo descrittivo.
    """

    # Diagnosi con descrizioni ICD-9
    diag_path = os.path.join(base_path, "DIAGNOSES_ICD.csv")
    icd_path  = os.path.join(base_path, "D_ICD_DIAGNOSES.csv")

    if os.path.exists(diag_path) and os.path.exists(icd_path):
        try:
            diag = pd.read_csv(diag_path)
            icd  = pd.read_csv(icd_path, usecols=["ICD9_CODE", "LONG_TITLE"])
            merged = (
                diag.merge(icd, on="ICD9_CODE", how="left")
                    .dropna(subset=["LONG_TITLE"])
            )

            for title, group in merged.groupby("LONG_TITLE"):
                count = len(group)
                yield {
                    "text": (
                        f"Diagnosi clinica osservata: {title}. "
                        f"Registrata in {count} casi nel dataset MIMIC-III demo. "
                        f"Codice ICD-9: {group['ICD9_CODE'].iloc[0]}."
                    ),
                    "source": "mimic_demo/diagnoses"
                }
        except Exception as e:
            print(f"[mimic_loader] Errore diagnosi demo: {e}")

    # Procedure
    proc_path = os.path.join(base_path, "PROCEDURES_ICD.csv")
    icd_proc  = os.path.join(base_path, "D_ICD_PROCEDURES.csv")

    if os.path.exists(proc_path) and os.path.exists(icd_proc):
        try:
            proc = pd.read_csv(proc_path)
            icd  = pd.read_csv(icd_proc, usecols=["ICD9_CODE", "LONG_TITLE"])
            merged = (
                proc.merge(icd, on="ICD9_CODE", how="left")
                    .dropna(subset=["LONG_TITLE"])
            )

            for title, group in merged.groupby("LONG_TITLE"):
                count = len(group)
                yield {
                    "text": (
                        f"Procedura clinica: {title}. "
                        f"Eseguita in {count} casi nel dataset MIMIC-III demo."
                    ),
                    "source": "mimic_demo/procedures"
                }
        except Exception as e:
            print(f"[mimic_loader] Errore procedure demo: {e}")

# def load_mimic(base_path="data/mimiciii-demo/1.4"):

    # possible_files = [
    #     "NOTEEVENTS.csv",
    #     "NOTEEVENTS.csv.gz",
    #     "NOTEEVENTS_subset.csv"
    # ]

    # file_path = None

    # for f in possible_files:
    #     p = os.path.join(base_path, f)
    #     if os.path.exists(p):
    #         file_path = p
    #         break

    # if file_path is None:
    #     raise ValueError("NOTEEVENTS non trovato nel dataset demo")

    # if file_path.endswith(".gz"):
    #     df = pd.read_csv(file_path, compression="gzip")
    # else:
    #     df = pd.read_csv(file_path)

    # # estrazione testi clinici
    # for _, row in df.iterrows():
    #     text = row.get("TEXT", "")

    #     if isinstance(text, str) and len(text) > 200:
    #         yield {
    #             "text": text[:1000],
    #             "source": "mimic"
    #         }