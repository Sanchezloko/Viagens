"""
Envia uma mensagem de teste via CallMeBot pra validar se o WhatsApp está chegando.

Uso (a partir de flight-tracker/):
    python -m scripts.test_notify
"""
import sys
import requests
from app import config


def main():
    if not config.CALLMEBOT_PHONE or not config.CALLMEBOT_APIKEY:
        print("! CALLMEBOT_PHONE e CALLMEBOT_APIKEY não configurados no .env")
        return 1

    msg = "🛫 Teste do Flight Tracker — se você tá lendo isso no WhatsApp, deu certo!"
    print(f"Enviando pra +{config.CALLMEBOT_PHONE}...")

    r = requests.get(
        "https://api.callmebot.com/whatsapp.php",
        params={
            "phone": config.CALLMEBOT_PHONE,
            "text": msg,
            "apikey": config.CALLMEBOT_APIKEY,
        },
        timeout=15,
    )
    print(f"Status HTTP: {r.status_code}")
    print(f"Resposta: {r.text[:300]}")

    if r.status_code == 200 and "ERROR" not in r.text.upper():
        print("\n✓ Cheque seu WhatsApp em até 30s.")
        return 0

    print("\n✗ Falhou. Verifique:")
    print("  - número está correto e formato 5511999999999 (sem +)")
    print("  - apikey foi gerada (mande a frase de ativação no WhatsApp)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
