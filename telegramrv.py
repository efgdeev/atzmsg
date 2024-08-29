from telethon import TelegramClient, events, types
import re
from collections import deque
from datetime import datetime, time
import asyncio
import os  # Import necessário para verificar o arquivo

api_hash = 'bca4aa9933a9cc1432cb1f6c3668e3c0'
api_id = 23607721

sessao = 'Repassar Mensagem'
historico = deque(maxlen=50)

substituicoes = {
    't.me/panoramajonasesteves': '**EFG Market Mind:** O segredo dos grandes PLAYERS para operar, solicite nossa grade de estudos! @servidorefg',
    '''Via Terminal Macro Trader / ActivTrades

...
Disclaimer ActivTrades Brasil: Os derivativos financeiros são instrumentos complexos e apresentam um alto risco de perder dinheiro rapidamente devido à alavancagem. 83% das contas de investidores de retalhos perdem dinheiro quando negociam derivativos''':'''**EFG Market Mind:**

...
Os derivativos são complexos e apresentam alto risco de perda rápida. 80% dos investidores de retalho perdem dinheiro. Nossa mentoria e estratégias de investimento capacitam você com conhecimento e ferramentas para decisões mais informadas e redução de riscos.''',
    'Mais sobre o Panorama:': '**EFG Market Mind**',
    '''🔴 Em 15 Minutos

Material exclusivo do Terminal Macro Trader:

Acompanhe Ao Vivo o MacroClose - Com Júnior Wuttke (CNPI-P) da Macro Trader (17:30)''':'',
'Panorama Jonas Esteves': '',
'Assine o Panorama e garanta seus 7 dias gratuitos.': '',
'''🔴 A preparação completa está disponível apenas no Terminal Macro Trader. Cliente ActivTrades tem acesso gratuito. Acesse: https://www.macrotrader.com.br/terminal
    
   via Terminal Macro Trader/Activtrades

...
Disclaimer ActivTrades Brasil: Os derivativos financeiros são instrumentos complexos e apresentam um alto risco de perder dinheiro rapidamente devido à alavancagem. 82% das contas de investidores de retalhos perdem dinheiro quando negociam derivativos''':'',
'''🔴 Em 15 Minutos

Material exclusivo do Terminal Macro Trader:

Acompanhe Ao Vivo o MacroPreps - Com Júnior Wuttke (CNPI-P) da Macro Trader (8h)

YouTube/MacroTrader''':'',

}

# Função para substituir o texto e links
def substituir_texto_e_links(mensagem):
    for antigo, novo in substituicoes.items():
        mensagem = mensagem.replace(antigo, novo)
    mensagem = re.sub(r'@[^\s]+', '', mensagem)  # Remover menções
    return mensagem

# Função para verificar se a mensagem já foi enviada
def mensagem_repetida(mensagem):
    return any(mensagem == antiga for antiga in historico)

# Função para processar e enviar a mensagem
async def processar_mensagem(event):
    mensagem_modificada = substituir_texto_e_links(event.raw_text)

    if not mensagem_repetida(mensagem_modificada):
        destino = -1002231747942
        if event.media:
            if isinstance(event.media, types.MessageMediaWebPage):
                await event.client.send_message(destino, mensagem_modificada)
            else:
                await event.client.send_file(destino, file=event.media, caption=mensagem_modificada)
        else:
            await event.client.send_message(destino, mensagem_modificada)

        historico.append(mensagem_modificada)

# Função para enviar a imagem com texto nos horários específicos
async def enviar_imagem_em_horarios_especificos(client):
    destino = -1002231747942
    image_path = '/home/kaioluan2013_km/Curso_Feed.png'
    texto = '''**EFG Market Mind:**
**Você está pronto para transformar seu conhecimento e alcançar o próximo nível?**

Este é o momento de agir e conquistar a independência financeira que você sempre sonhou! No curso **Domine Estratégias Lucrativas no Mercado Financeiro**, você aprenderá com profundidade sobre:
- **macroeconomia**,
- **paridade e correlação**,
- **estratégias poderosas de daytrade e swingtrade**,
e terá **acesso exclusivo a indicadores** desenvolvidos para maximizar seus ganhos.

💡 **Bônus Especial:** Receba todos os modelos matemáticos transformados em indicadores que serão o diferencial nas suas operações. E o melhor, você pode começar agora mesmo investindo apenas **12x de R$ 115,83**.

💰 **Não deixe passar essa oportunidade**

cada dia de espera é um dia a menos de ganhos potenciais. **Inscreva-se já e domine o mercado financeiro!**'''

    # Verifica se o caminho da imagem é válido
    if not os.path.exists(image_path):
        print(f"Erro: A imagem '{imagem_caminho}' não foi encontrada.")
        return

    # Defina os horários específicos
    horarios_especificos = [time(10, 0), time(13, 30), time(00, 18)]

    while True:
        agora = datetime.now().time()
        for horario in horarios_especificos:
            if agora.hour == horario.hour and agora.minute == horario.minute:
                await client.send_file(destino, imagem_caminho, caption=texto)
                print(f"Imagem enviada às {horario}")
                await asyncio.sleep(60)  # Aguarda 60 segundos para evitar reenvio dentro do mesmo minuto

        await asyncio.sleep(1)  # Verifica a cada segundo

def main():
    print('Monitoramento iniciado ...')
    client = TelegramClient(sessao, api_id, api_hash)

    @client.on(events.NewMessage(chats=[-1001744113331, -1001257215455]))
    async def handle_new_message(event):
        agora = datetime.now().time()

        if event.chat_id == -1001257215455 and agora >= datetime.strptime("18:20", "%H:%M").time():
            return  # Ignora a mensagem fora do horário permitido

        if event.chat_id == -1001744113331:
            try:
                await client.get_entity(event.chat_id)
            except Exception:
                print(f"Erro ao acessar o canal ID {event.chat_id}. Tentando forçar a transferência.")
                await processar_mensagem(event)
                return

        await processar_mensagem(event)

    client.start()
    client.loop.create_task(enviar_imagem_em_horarios_especificos(client))
    client.run_until_disconnected()

main()
