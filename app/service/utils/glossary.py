import re

class GlossaryTerm:
    def __init__(self, term, pronunciation=None, variations=None):
        self.term = term
        self.pronunciation = pronunciation
        self.variations = variations or []

GLOSSARY = {
    # Términos técnicos
    "FORUS": GlossaryTerm("FORUS", variations=["forus", "Forus", "4us"]),
    "URL": GlossaryTerm("URL", variations=["url", "Url", "U.R.L."]),

    "RUT": GlossaryTerm("RUT", variations=["root", "rut", "Root"]),
    "OC (Orden de Compra)": GlossaryTerm("OC", variations=["oc", "orden de compra", "Orden de Compra"]),

}

def apply_glossary(text):
    """
    Aplica el glosario al texto para corregir términos específicos.
    """
    processed_text = text

    for term_key, term_obj in GLOSSARY.items():
        # Crear patrón de regex que incluye el término principal y sus variaciones
        variations = [re.escape(var) for var in [term_obj.term] + term_obj.variations]
        pattern = '|'.join(variations)

        # Reemplazar todas las variaciones con el término correcto
        processed_text = re.sub(
            pattern,
            term_obj.term,
            processed_text,
            flags=re.IGNORECASE
        )

    return processed_text