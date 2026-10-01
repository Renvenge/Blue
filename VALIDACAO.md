# Validação do Blue 0.3

ISO final compilada em 01/10/2026 e testada em VirtualBox 7.0.8, na VM Blue com UEFI, duas CPUs, 2 GB de RAM, VMSVGA e disco persistente de 32 GB. SHA256: `02736f2d542175f199b4d07838876b8f668c7dc8591e38f81c4fc52c4c078665`. Tamanho: 1.511.817.216 bytes. Checksum conferido depois da transferência.

- Persistência: criado um arquivo na pasta do usuário e instalado `tree` 2.2.1-1 pelo APT. Após desligamento seguro e nova inicialização, o conteúdo do arquivo permaneceu e o programa executou normalmente. A montagem raiz usa a partição ext4 `blue-data` como camada gravável. Relatório: `evidencias/persistencia-03.txt`; instalação: `evidencias/apt-03.log`.
- Ferramentas: as 20 verificações de `blue-check-tools` passaram na imagem final reiniciada, incluindo compilação e execução C/C++, Python/venv/pip, Node/npm, Git, SQLite, CMake e GDB. Relatório: `evidencias/tools-03.json`.
- Tela: o cliente acompanhou os pedidos de resolução do VirtualBox em 1024 × 640, 800 × 600 e 1280 × 720. Na inicialização final, iniciou automaticamente e respondeu novamente aos pedidos de 1024 × 640 e 800 × 600. O assistente cabe inteiro em 800 × 600. Capturas: `evidencias/desktop-03-final.png` e `evidencias/assistente-03-800.png`; registro de redimensionamento: `evidencias/display-03.log`.
- Desktop: barra inferior única, Lixeira, papel de parede original e assistente minimizado na abertura. Nenhum painel de boas-vindas abre automaticamente.
- Código: cinco testes do assistente e cinco testes das verificações de disco passaram. O preparador de disco recusa número de série errado, partições existentes, sistema de arquivos, disco montado e assinaturas prévias nos setores verificados.

A imagem final usa um único sistema compactado. Isso elimina o conflito de prioridade entre camadas que foi encontrado com a persistência. O cliente gráfico tem acesso apenas à interface `vboxuser` pelo grupo `video`, com modo 0660; `vboxguest` continua restrito ao administrador. VBoxClient/VBoxService 7.0.8 usam os drivers já presentes no kernel Debian.

Esta edição é Live com persistência, sem instalador: mantenha a ISO conectada à VM. A VM Blue-Test e suas imagens anteriores foram preservadas. O teste da versão 0.3 cobre UEFI em VirtualBox; Secure Boot e hardware físico não foram validados. A conversa com IA continua dependendo de um modelo local separado, conforme ASSISTENTE.md.

## Histórico: Blue 0.2

Imagem compilada em 01/10/2026, com base Debian 13 amd64. Testes em VirtualBox 7.0.8, com duas CPUs e 2 GB de RAM, sem disco instalado na máquina de teste.

## Resultados

- Inicialização BIOS: sessão gráfica LXDE, login automático e Blue Assistant funcionando.
- Inicialização UEFI: mesma ISO chegou à sessão gráfica LXDE com login automático e Blue Assistant funcionando, sem Secure Boot.
- `blue-check-tools`: 20 verificações aprovadas durante a compilação e novamente como usuário `blue` na ISO final. Inclui compilação e execução C/C++, Python, ambiente virtual e pip, Node.js, projeto npm, Git, SQLite, CMake, GDB, Geany, ShellCheck, ripgrep, jq, pkg-config e APT.
- Instalação real: atualização dos repositórios e instalação do pacote `hello` pelo APT, ambas concluídas. O programa instalado executou “Olá, mundo!”. Nenhuma correção manual foi necessária na sessão da ISO final.
- Assistente: cinco testes automatizados aprovados. Interface, monitor de recursos e indicação do aplicativo ativo conferidos no desktop. Cliente de chat verificado com servidor simulado; não foi incluído um modelo de linguagem.
- SHA256 da ISO transferida conferido com o resultado da compilação: `4b0befb2a0c28022f29e04044ae9c5dd20a8fe54a334ab79e78be3adda4dd4cb`.
- Tamanho: 1.482.964.992 bytes (1,48 GB decimal).

## Correções incorporadas

O carregador de inicialização usa kernels que realmente estão no sistema compactado. A imagem contém um módulo nativo do Debian Live que restaura o auxiliar `start-stop-daemon` original do pacote dpkg, ausente após uma etapa de limpeza do live-build. O arquivo é conferido contra o checksum do pacote, permitindo a instalação normal pelo APT.

## Limites desta entrega

Edição Live sem instalador de disco e sem persistência configurada. Programas e mudanças da sessão se perdem após reiniciar. Não foram testados Secure Boot, hardware físico, áudio, todos os modelos de Wi-Fi/GPU ou todo software disponível. As ferramentas incluídas e um exemplo real de instalação foram testados; isso não garante compatibilidade universal.

O monitor local funciona. A conversa com IA exige instalar e iniciar um modelo/backend local compatível, conforme ASSISTENTE.md. Ainda não há integração para compreender o conteúdo do editor nem voz.

As capturas de tela e o relatório de ferramentas estão em `evidencias/`.

## Edição com interface moderna

Arquivo separado: `Blue-0.2-modern.iso`. SHA256: `590154432d5789409dd587871cff2313069cde82e8f4ab213b96f47cccd3d5a3`. Mesmo tamanho da edição anterior. A ISO anterior foi preservada para a VM já aberta.

Inicialização UEFI conferida na VM Blue-Preview: tela Início do Blue, seis atalhos, assistente minimizado, atalhos no desktop e barra inferior maior. A resolução inicial foi ajustada automaticamente para 800 × 600 em VirtualBox; a janela inteira e a barra ficaram visíveis. Captura: `evidencias/desktop-moderno.png`. Cinco testes do assistente continuam aprovados.

Na ISO moderna, as 20 verificações de ferramentas e a atualização/instalação do pacote `hello` também passaram novamente. Captura: `evidencias/teste-modern.png`.

O atalho do gerenciador gráfico usa o caminho completo `/usr/sbin/synaptic`; sua abertura pelo polkit foi conferida, conforme `evidencias/synaptic-moderno.png`. Esse ajuste final foi incorporado à imagem após os testes das ferramentas, sem alterar os pacotes ou o monitor.

## Edição minimalista

Arquivo `Blue-0.2-minimal.iso`, SHA256 `040a809259d25e02a8005c3523473d9a07133c3d6507d35f472727f0a364525a`. Checksum conferido após transferir a ISO. Mantém os pacotes da edição moderna, alterando a apresentação do desktop: tela inicial desativada, ícones do desktop ocultos, barra superior fina e dock com ícones vetoriais simples. Os cinco testes do assistente continuam aprovados.

Inicialização UEFI da imagem final conferida em Blue-Minimal, com 1 GB de RAM e duas CPUs. A sessão abriu em 800 × 600 com desktop sem ícones, menu e relógio no topo, dock com símbolos distintos e assistente minimizado. Captura real: `evidencias/desktop-minimal.png`. A VM foi deixada configurada com 2 GB para uso posterior. O teste de 1 GB cobre a abertura da sessão; não mede o desempenho em projetos grandes ou modelos de IA.

## Layout original atualizado

Arquivo atual `Blue-0.2-classic.iso`, SHA256 `44904a75267baa2d6052ba4bb75846ceb6e62c0019c930f5f57ccc44da0070f8`. Os pacotes e as ferramentas foram mantidos. A barra original voltou à parte inferior e o desktop mostra a Lixeira; o tema Openbox Blue atualiza o acabamento das janelas com cores planas e bordas discretas. A tela inicial permanece desativada na abertura da sessão.

A camada de atualização é recriada para não conservar o dock de uma edição anterior. A configuração do usuário para Openbox preserva os atalhos existentes e aplica o tema apenas na primeira sessão.

Imagem final inicializada em UEFI na Blue-Test com 2 GB e duas CPUs. Conferidos a barra inferior única, a Lixeira, o tema plano Blue e o assistente funcionando. Em 800 × 600, a janela foi ajustada à resolução real: caixa de texto, botão Enviar e barra inferior permanecem totalmente visíveis. Capturas: `evidencias/desktop-classic.png` e `evidencias/janela-classic.png`. Cinco testes do assistente aprovados; checksum da ISO final conferido após a transferência.
