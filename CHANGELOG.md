# Histórico de versões

As datas registram o desenvolvimento local. Elas não indicam que uma release já foi publicada no GitHub.

## 0.3 — 2026-10-01

- Persistência completa em volume ext4 `blue-data`, para arquivos, configurações e programas.
- Integração de tela com VBoxClient/VBoxService 7.0.8 e drivers do kernel Debian.
- Permissão de vídeo restrita ao grupo `video` na interface `vboxuser`.
- Sistema compactado único para evitar conflitos de camadas com persistência.
- Desktop com barra inferior original, tema Blue e assistente minimizado.
- Verificadas 20 operações de programação, instalação pelo APT e preservação de dados após nova inicialização.
- Documentação para publicação, autoria de Renvenge e créditos de terceiros.

## 0.2 — 2026-10-01

- Base Debian 13 amd64, desktop LXDE/Openbox e identidade Blue.
- Ferramentas de desenvolvimento, APT, Synaptic e zram.
- Protótipo do assistente: monitor local e cliente para modelo separado.
- Testes de boot BIOS/UEFI e verificações das ferramentas.
- Revisões experimentais da interface até retornar à organização original com acabamento atualizado.

Os nomes `modern`, `minimal` e `classic` identificam imagens locais de avaliação da versão 0.2. Consulte [VALIDACAO.md](VALIDACAO.md) para os resultados de cada imagem.
