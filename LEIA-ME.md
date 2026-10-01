# Blue 0.3

Criado e mantido por **Renvenge**, com auxílio de ferramentas de IA. Para a apresentação pública e o índice completo dos guias, consulte [README.md](README.md). Este arquivo conserva as instruções da entrega local.

Projeto open source de distribuição Linux leve voltada à programação para computadores x86_64, com base Debian 13 (trixie), desktop LXDE e logo de círculo azul irregular. Esta entrega contém a ISO compilada, os arquivos de construção e a identidade visual. Os resultados dos testes estão em VALIDACAO.md.

## O que está incluído

- Kernel Linux e base Debian, sessão LXDE/Openbox e gerenciador de arquivos PCManFM.
- Geany, Git, ferramentas C/C++, Python, Node.js/npm, depurador, terminal e navegador para documentação.
- Blue Assistant: protótipo de monitor local com interface e cliente de IA; veja ASSISTENTE.md.
- Idioma e teclado brasileiros; fuso America/Fortaleza.
- Compressão de memória com zram, sem compositor e sem suíte de escritório.
- Logo SVG/PNG, papel de parede, menu Blue e página de boas-vindas.
- Receita Live ISO híbrida com inicialização BIOS/UEFI, sem instalador de disco.

## Interface atualizada

A edição atual é Blue-0.3-amd64.iso: mantém a organização da primeira versão, com a Lixeira no desktop e uma única barra inferior para menu, aplicativos e relógio. O acabamento usa cores azul-escuras, barra discreta e bordas de janela planas. O assistente inicia minimizado.

Em VirtualBox, a primeira sessão usa 800 × 600 para caber em notebooks. Depois, o cliente de vídeo acompanha o tamanho da janela com o controlador VMSVGA. No menu Visualizar do VirtualBox, mantenha habilitado o ajuste automático da tela do convidado. O ajuste manual continua disponível no aplicativo Início do Blue, aberto pelo menu.

## Arquivos e programas salvos

A VM **Blue** preparada nesta entrega usa um disco virtual separado de 32 GB, `Blue-0.3-data.vdi`, para preservar arquivos, configurações e programas instalados. Abra essa VM no VirtualBox e inicie normalmente. Desligue pelo menu do Linux para que os dados sejam gravados corretamente.

Mantenha a ISO conectada ao leitor virtual: esta é uma edição Live com persistência, ainda sem instalador de disco. Para fazer uma cópia de segurança, desligue a VM e copie o VDI. A antiga Blue-Test continua separada; seus arquivos não são transferidos automaticamente para a nova VM.

A ISO sozinha também inicia, mas as mudanças só permanecem se houver um volume ext4 com rótulo `blue-data` e arquivo `persistence.conf` contendo `/ union`. Os parâmetros de boot já procuram esse volume. O script `scripts/prepare-data-disk.py` prepara apenas um novo disco VirtualBox vazio, conferindo seu número de série; não use em discos com arquivos.

## Gerar a ISO

Use uma máquina ou VM **Debian 13 amd64**, com internet e ao menos 20 GB livres. Copie este diretório para o sistema de arquivos Linux da máquina; evite compilar diretamente em uma pasta Windows compartilhada.

```sh
sudo apt update
sudo apt install python3 live-build debootstrap xorriso squashfs-tools dosfstools mtools isolinux syslinux-common grub-pc-bin grub-efi-amd64-bin
sudo bash scripts/prepare-vbox-tools.sh /caminho/VBoxGuestAdditions_7.0.8.iso
sudo bash build-blue.sh
```

Saída esperada: `Blue-0.3-amd64.iso` e `Blue-0.3-amd64.iso.sha256`. O preparador confere o SHA256 dos Guest Additions oficiais 7.0.8. Cada tentativa conserva seu diretório e log em `build/iso-*`. A compilação baixa pacotes Debian; a receita usa versões disponíveis no repositório, portanto não garante imagens binariamente idênticas entre datas.

## Testar antes de usar

Primeiro inicie a ISO em uma máquina virtual, com 2 GB de RAM e duas CPUs como configuração inicial de teste. Confira login automático, resolução da tela, teclado brasileiro, rede, áudio, menu, abertura de aplicativos e desligamento. Repita em BIOS e UEFI. Secure Boot não foi validado.

No Linux, um teste BIOS pode ser iniciado com:

```sh
qemu-system-x86_64 -m 2048 -smp 2 -cdrom Blue-0.3-amd64.iso -boot d
```

Use 2 GB de RAM e duas CPUs como ponto de partida, sem modelo de IA carregado. Firefox, projetos grandes e modelos de IA podem exigir mais memória. Veja os testes de cada edição em VALIDACAO.md.

## Instalar ferramentas e bibliotecas

O Blue é focado em programação, mas não bloqueia a instalação de outros programas. APT e Synaptic estão incluídos. Na sessão Live, use `sudo apt update` e `sudo apt install nome-do-pacote`. Instale bibliotecas Python dentro de um ambiente virtual (`python3 -m venv .venv`); o Debian protege seu Python de sistema contra instalações globais por pip. Dependências JavaScript podem ser instaladas normalmente por npm no seu projeto.

Na VM Blue com o disco de persistência, as instalações permanecem depois de reiniciar. Sem esse disco, as instalações feitas na sessão Live se perdem.

Execute `blue-check-tools` no terminal para compilar exemplos C/C++, criar um ambiente Python, executar Python/Node/npm, testar Git, SQLite, CMake e GDB e conferir Geany/APT. O mesmo teste roda durante a construção e interrompe a geração se alguma ferramenta falhar.

## Sessão Live

A persistência desta edição segue o [manual do Debian Live](https://live-team.pages.debian.net/live-manual/html/live-manual/customizing-run-time-behaviours.en.html). O redimensionamento utiliza VBoxClient/VBoxService 7.0.8, com os drivers do kernel Debian. Os componentes VirtualBox mantêm a licença GPLv3 em `config/includes.chroot/usr/lib/blue-vbox/LICENSE`; o endereço do código-fonte oficial está em `SOURCE.txt` no mesmo diretório. Não é necessário instalar o Extension Pack.

O usuário `blue` entra automaticamente. A sessão Live padrão do Debian concede sudo ao usuário Live. Use para teste em um computador sob seu controle. As mudanças não permanecem após reiniciar sem configurar persistência. Esta versão não instala o Blue no disco.

## Identidade e personalização

Abra `preview.html` para ver a proposta visual. Ela é apenas uma prévia gráfica. A logo está em `assets/blue-logo.svg` e `assets/blue-logo.png`; o papel de parede em `assets/blue-wallpaper.png`. Os arquivos em `config/includes.chroot` são copiados para o sistema e `config/package-lists/blue.list.chroot` define os programas.

O código original, scripts e arte original do Blue estão sob licença MIT (LICENSE). Os componentes Debian preservam suas próprias licenças. A receita usa apenas o repositório main, sem firmware proprietário; isso pode limitar Wi-Fi/GPU em alguns computadores. O modelo de IA não está incluído e deve ser escolhido com licença compatível. O código está disponível neste projeto local, ainda sem repositório público. Antes de distribuir uma ISO publicamente, confira obrigações de licenciamento e disponibilização do código-fonte dos pacotes incluídos.

Referências: https://live-team.pages.debian.net/live-manual/html/live-manual.en.html e https://manpages.debian.org/trixie/live-build/lb_config.1.en.html
