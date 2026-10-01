# Publicar no GitHub

## Preparar o repositório

Use o pacote `Blue-0.3-github.zip` preparado com fontes, documentação, arte e evidências. Extraia a pasta Blue e coloque **seu conteúdo** na raiz do repositório, para que `README.md` apareça na página inicial.

O pacote público não contém a pasta local `build-tools`, senhas, ambientes auxiliares, discos de VM ou ISOs. Os executáveis VirtualBox também ficam fora desse pacote; a receita explica como obtê-los da imagem oficial.

Uma descrição curta para o repositório:

> Distribuição Linux leve baseada no Debian, voltada à programação e criada por Renvenge.

Tópicos possíveis: `linux`, `debian`, `live-build`, `lxde`, `open-source`, `developer-tools`.

O pseudônimo Renvenge está registrado nos créditos e na licença do código original. O projeto não pressupõe que esse também seja o nome da sua conta no GitHub; os links internos funcionam independentemente do endereço escolhido.

## Publicar uma release

Publique a ISO como anexo de uma release, separadamente das fontes do repositório. O GitHub bloqueia arquivos acima de 100 MiB no Git comum; a ISO 0.3 tem aproximadamente 1,51 GB. Veja a [documentação oficial de arquivos grandes](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

Itens da release:

- `Blue-0.3-amd64.iso`.
- `Blue-0.3-amd64.iso.sha256` correspondente à mesma imagem.
- `Blue-0.3-amd64.packages`.
- Fontes originais do Blue correspondentes à construção.
- Fontes correspondentes e avisos exigidos pelas licenças dos componentes redistribuídos.

Para o código dos pacotes Debian, use o manifesto exato da imagem e as licenças de cada pacote como referência. A receita pode baixar versões diferentes em outra data; não substitua a coleção de fontes da release por uma nova construção sem comparar versões. Para os clientes VirtualBox, preserve a licença e as fontes oficiais 7.0.8.

A documentação e o manifesto ajudam nessa preparação, mas o pacote de fontes do Blue sozinho não é uma coleção completa das fontes de todos os programas contidos na ISO. Consulte [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

## Texto da release 0.3

> Blue 0.3 é uma distribuição Linux experimental baseada no Debian 13, criada e mantida por Renvenge para programação. Inclui desktop LXDE/Openbox, ferramentas de desenvolvimento, persistência em disco preparado e ajuste de tela no VirtualBox. O assistente monitora recursos localmente; a conversa com IA exige um modelo e um servidor separados. Esta edição funciona como Live com persistência e ainda não oferece instalador de disco. Os testes da versão cobrem UEFI no VirtualBox 7.0.8.

Inclua o link para VALIDACAO.md e indique que a ISO precisa continuar conectada quando usada com o disco persistente. Não publique seu VDI pessoal como se fosse um instalador.

## Depois da publicação

Habilite o canal privado de relato de vulnerabilidades se quiser oferecer o fluxo descrito em SECURITY.md. Atualize o README com o endereço real da release e registre mudanças futuras no CHANGELOG. Nenhuma publicação ou conta externa foi criada por estes arquivos.
