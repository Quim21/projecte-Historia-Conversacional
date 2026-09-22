from excepcions.errors import OrdreInvalida

VERBS_VALIDS = {
    "ANAR",
    "AGAFAR",
    "DEIXAR",
    "USAR",
    "ENCENDRE",
    "APAGAR",
    "OBRIR",
    "TANCAR",
    "PARLAR",
}


def interpretar(text):
    parts = text.strip().split(maxsplit=1)
    if not parts:
        raise OrdreInvalida(text)

    verb = parts[0].upper()
    objectiu = parts[1].strip() if len(parts) > 1 else None

    if verb not in VERBS_VALIDS:
        raise OrdreInvalida(text)

    return verb, objectiu
