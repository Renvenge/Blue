# Privacidade do Blue Assistant

Esta descrição cobre o código do assistente incluído na versão 0.3. Outros aplicativos e o servidor de modelo local têm comportamentos próprios.

## Monitoramento

Enquanto o monitor está ativo, a cada cinco segundos o assistente consulta:

- Utilização de CPU.
- Memória disponível e usada.
- Ocupação do sistema de arquivos que contém a pasta pessoal.
- Classe do aplicativo cuja janela está ativa na sessão X11.

Ele não captura teclas, screenshots, áudio, conteúdo de arquivos ou títulos das janelas. Identificar a classe do editor aberto não significa ler seu código ou compreender o que você está programando.

O botão de pausa interrompe a coleta. Encerrar o assistente encerra o programa. A janela minimizada mantém o monitor ativo.

## Conversa com o modelo

Quando o usuário envia uma pergunta, o cliente envia essa pergunta e a última amostra de recursos para `http://127.0.0.1:8080/v1/chat/completions`. Não transmite amostras continuamente. Cada pergunta é independente; a conversa mostrada na interface não é enviada como histórico.

O cliente ignora proxies e bloqueia redirecionamentos. Não há serviço de IA na nuvem configurado no código atual. Um servidor local não está incluído nem é baixado automaticamente.

## Retenção

O assistente não salva conversas em disco. O texto permanece na memória da sessão até limpar a conversa ou fechar o programa. Essa descrição não significa que o sistema operacional nunca possa gravar memória em swap ou que o servidor de modelo não mantenha seus próprios logs.

Configure o backend separadamente conforme suas necessidades. O assistente não controla a política de retenção desse servidor e não executa os comandos sugeridos pelo modelo.
