import pandas as pd
from telethon import TelegramClient, events
from telethon.tl.custom import Button
import main as m  

client = TelegramClient('session_name_5', m.api_id, m.api_hash).start(bot_token=m.TOKEN)

df = pd.read_excel(r"C:\Users\Hp\Desktop\Safra\safra_parfum.xlsx")

async def get_keyboard():
    return [
        [Button.text("Ətir Əlavə Et")]
    ]


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    keyboard = await get_keyboard()
    await event.respond("Salam, Elegans Bota Xoş gəlmisiniz!")

@client.on(events.NewMessage)
async def handle_message(event):
    message = event.message.message.strip()

    if message == "/start":
        return

    if message == "Ətir Əlavə Et":
        await event.respond("Zəhmət olmasa ətirin adını, qiymətini və ya 'qiymət ml' şəklində yazın (məs: 0.51 30):")
        return

    parts = message.split(",")

    try:
     
        if len(parts) == 2:
            deyer, miqdar = parts
            response = await calculate_perfume_price(deyer, miqdar)
            await event.respond(response)
            return

        elif len(parts) == 1 and is_float(parts[0]):
            response = await calculate_perfume_prices_ml(parts[0])
            await event.respond(response)
            return

    except Exception:
        pass 


    await search_perfume_by_name(event, message)

def is_float(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


async def search_perfume_by_name(event, parfum_text):
    try:
        words = parfum_text.lower().split()
        mask = df['etir'].str.lower().apply(lambda x: all(word in x for word in words))
        parfums = df.loc[mask, ['etir', 'qiymet']]

        if not parfums.empty:
            response = "\n".join([f"{row['etir']} - {row['qiymet']} AZN" for _, row in parfums.iterrows()])
            await event.respond(response)
        else:
            await event.respond("Axtardığınız parfüm tapılmadı.")
    except Exception as e:
        await event.respond(f"Xəta baş verdi: {str(e)}")


async def calculate_perfume_price(deyer, miqdar):
    try:
        deyer = float(deyer.strip())
        miqdar = int(miqdar.strip())
        umumi_qiymet = (
            deyer * (miqdar * 0.43)
            + (miqdar * 0.57) * m.parfum_suyu
            + m.kagiz + m.kisə + m.klok + m.lazer + m.qab + m.vinil
        ) * 1.3 * 2.5
        yum = round(umumi_qiymet, 0)
        return f"Seçdiyiniz parfümün {miqdar}ML qiyməti {yum} AZN-dır."
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"


async def calculate_perfume_prices_ml(deyer):
    try:
        deyer = float(deyer)
        ml = [10, 20, 30, 50, 100]
        um_metn = []
        for i in ml:
            umumi_qiymet = (
                deyer * (i * 0.43)
                + (i * 0.57) * m.parfum_suyu
                + m.kagiz + m.kisə + m.klok + m.lazer + m.qab + m.vinil
            ) * 1.3 * 2.5
            yum = round(umumi_qiymet, 0)
            um_metn.append(f"{i}ML - {yum} AZN")
        return "\n".join(um_metn)
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"

client.run_until_disconnected()
