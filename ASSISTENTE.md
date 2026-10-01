# Blue Assistant — incluído no Blue 0.3

O assistente é inspirado no conceito da Quarta. É uma implementação própria para Linux, não uma cópia do executável Windows ou dos modelos da Quarta.

## Implementado

- Monitor iniciado junto com a sessão LXDE; janela minimizada na edição com a interface atualizada.
- Amostra de CPU, memória, ocupação do disco que contém a pasta pessoal e classe do aplicativo ativo a cada cinco segundos.
- Pausar/retomar monitor, limpar conversa e encerrar assistente.
- Cliente de conversa para servidor local compatível com Chat Completions na porta 8080.
- Envia a pergunta e somente a última amostra ao modelo quando o usuário pergunta. Não envia amostras continuamente.
- Sem histórico em disco. Sem screenshots, títulos de janela, captura de teclas, microfone ou leitura automática de arquivos.
- Sem execução de comandos sugeridos pela IA. Não roda como root.

Saber que o editor está aberto não permite entender o código ou a intenção da pessoa. Acompanhamento de projeto, análise de erros e integração com o editor são próximos passos; ainda não estão implementados. Nesta versão cada pergunta é independente.

## Experimentar a interface no Linux

```sh
sudo apt install python3-tk x11-utils
python3 assistant/blue_assistant.py
```

Para responder com IA, instale um servidor local, por exemplo llama.cpp, e um modelo GGUF com licença que permita o uso e distribuição desejados. O modelo e o servidor ainda não estão incluídos na ISO. Com `llama-server` instalado:

```sh
llama-server -m /caminho/para/modelo.gguf --host 127.0.0.1 --port 8080 -c 2048
```

Documentação do servidor: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Sem servidor/modelo, o monitor continua funcionando e a interface informa que a IA está indisponível. O cliente não usa proxies e bloqueia redirecionamentos. O servidor de modelo precisa ser configurado para não manter logs de conversa se desejar a mesma política de retenção do cliente.

O consumo de RAM da IA depende do modelo; o objetivo de leveza do desktop não garante execução de modelos em 1 ou 2 GB. Não baixamos modelos automaticamente.

## Validação

Cinco testes unitários cobrem contadores de CPU, cálculo de memória, ausência de coleta sem display, bloqueio de redirecionamento e formato da chamada local. A interface, coleta X11 e inicialização foram conferidas na ISO em VM. O cliente foi testado com servidor simulado; não foi validada uma conversa com um modelo real incluído na distribuição, pois não há modelo incluído. Veja VALIDACAO.md para as evidências.

```sh
cd assistant
python3 -m unittest -v
```
# Interface

O assistente inicia minimizado, mas seu monitor continua ativo. Abra pelo menu de aplicativos ou pela janela minimizada na barra inferior. A janela adapta seu tamanho à resolução inicial e usa cores escuras com botões de alto contraste.

