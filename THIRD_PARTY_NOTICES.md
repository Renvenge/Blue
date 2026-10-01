# Componentes de terceiros

A licença MIT do Blue cobre as fontes, scripts, documentação e arte originais do projeto. Ela não altera as licenças dos programas que compõem a distribuição.

## Base Debian e aplicativos

O Blue usa Debian 13 e pacotes de seu repositório `main`, incluindo Linux, LXDE, Openbox, Python, ferramentas GNU e os demais aplicativos listados no manifesto `Blue-0.3-amd64.packages`.

Não há uma única licença para todos esses pacotes. Na sessão Linux, consulte `/usr/share/doc/NOME-DO-PACOTE/copyright` e os arquivos de licença correspondentes. Preserve os créditos e cumpra as condições aplicáveis aos componentes redistribuídos.

Referência: [orientações do Debian para redistribuição](https://www.debian.org/doc/manuals/debian-faq/redistributing.en.html).

## VirtualBox Guest Additions 7.0.8

A integração utiliza VBoxClient e VBoxService extraídos da imagem oficial e verificada por checksum. Esses executáveis mantêm a licença GPLv3 fornecida pelo projeto de origem.

- [Licença preservada](config/includes.chroot/usr/lib/blue-vbox/LICENSE).
- [Referência de origem](config/includes.chroot/usr/lib/blue-vbox/SOURCE.txt).
- [Código-fonte oficial da versão 7.0.8](https://download.virtualbox.org/virtualbox/7.0.8/VirtualBox-7.0.8.tar.bz2).

O pacote preparado para o repositório não inclui esses executáveis: eles são extraídos durante a preparação da compilação. A ISO compilada os inclui. Uma URL de origem, isoladamente, não deve ser tratada como confirmação de que todas as obrigações de distribuição de binários foram atendidas; organize as fontes correspondentes ao publicar a ISO.

## Modelos de IA

Nenhum modelo de linguagem é distribuído com o Blue 0.3. Modelos e backends escolhidos pelo usuário têm licenças próprias. O projeto não declara uma licença única ou permissão de redistribuição para modelos externos.
