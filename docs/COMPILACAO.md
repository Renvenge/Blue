# Compilar a ISO

## Ambiente

Use Debian 13 amd64, internet e pelo menos 20 GB livres como ponto de partida. Reserve mais espaço se conservar várias tentativas. A construção foi realizada em uma VM Debian; uma pasta Linux local é preferível a uma pasta Windows compartilhada.

Na raiz das fontes do Blue:

```sh
sudo apt update
sudo apt install python3 live-build debootstrap xorriso squashfs-tools \
  dosfstools mtools isolinux syslinux-common grub-pc-bin grub-efi-amd64-bin
```

## Integração com VirtualBox

O repositório preparado para GitHub não inclui os executáveis de terceiros. Obtenha a imagem oficial [VBoxGuestAdditions 7.0.8](https://download.virtualbox.org/virtualbox/7.0.8/VBoxGuestAdditions_7.0.8.iso) e execute:

```sh
sudo bash scripts/prepare-vbox-tools.sh /caminho/VBoxGuestAdditions_7.0.8.iso
```

O script confere o SHA256 fixado, extrai VBoxClient e VBoxService e conserva a licença e a referência ao código-fonte. Utiliza os drivers do kernel Debian; não instala o Extension Pack nem compila os módulos antigos dos Guest Additions.

SHA256 esperado da imagem oficial:

```text
8d73e2361afbf696e6128ffa5e96d9f6a78ff32cb2cb54c727a5be7992be0b31
```

Referência: [checksums oficiais](https://download.virtualbox.org/virtualbox/7.0.8/SHA256SUMS).

## Construção

```sh
sudo bash build-blue.sh
```

Saídas na raiz do projeto:

- `Blue-0.3-amd64.iso`: imagem Live híbrida.
- `Blue-0.3-amd64.iso.sha256`: checksum dessa construção.
- `Blue-0.3-amd64.packages`: pacotes e versões da imagem.
- `build/iso-*/build.log`: log da tentativa correspondente.

Cada tentativa usa um diretório próprio. Os testes das ferramentas são executados durante a construção. A finalização confere os kernels disponíveis, aplica os arquivos do Blue ao sistema compactado e gera novamente a ISO e os checksums internos.

A receita usa pacotes disponíveis no repositório Debian. Novas execuções podem obter versões diferentes e produzir outro checksum; não há garantia de reprodução binária idêntica entre datas.

## Verificação

```sh
sha256sum -c Blue-0.3-amd64.iso.sha256
python3 -m unittest discover -s assistant -v
python3 -m unittest discover -s tests -v
```

Depois, inicie a ISO em uma VM e execute `blue-check-tools` como usuário `blue`. Confira rede, desktop, resolução e desligamento. Prepare um novo disco persistente e verifique arquivo e instalação após uma nova inicialização. Repita em BIOS e UEFI antes de ampliar os ambientes declarados como testados.

O relatório atual está em [VALIDACAO.md](../VALIDACAO.md). A compilação bem-sucedida não substitui o teste de boot da imagem resultante.
