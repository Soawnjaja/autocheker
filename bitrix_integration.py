from bitrix24 import Bitrix24

# Инициализация Bitrix24
bx24 = Bitrix24('https://yourcompany.bitrix24.com/rest/1/your_webhook')

def send_message_to_bitrix(message):
    bx24.callMethod('im.message.add', DIALOG_ID='chat1', MESSAGE=message)