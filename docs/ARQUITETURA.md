# Organização do Blue

Blue personaliza uma base Debian. O kernel, o gerenciador de pacotes e a maior parte dos aplicativos vêm dos projetos de base. As fontes deste repositório definem a construção, a identidade visual e os utilitários próprios.

| Caminho | Responsabilidade |
| --- | --- |
| `build-blue.sh` | Configuração e execução do live-build |
| `finalize-image.py` | Atualização do sistema compactado, conferência de kernels e geração final da ISO |
| `config/package-lists/` | Lista dos pacotes Debian incluídos |
| `config/hooks/live/` | Ajustes e verificações durante a construção |
| `config/includes.chroot/` | Arquivos copiados para o sistema Linux |
| `assistant/` | Monitor, interface, cliente de IA e testes |
| `scripts/` | Preparação dos clientes VirtualBox e do novo disco persistente |
| `tests/` | Verificações do preparador de disco |
| `assets/` | Logo, papel de parede e arte de inicialização |
| `evidencias/` | Relatórios e capturas dos testes documentados |
| `docs/` | Guias de uso, construção e publicação |

## Inicialização e persistência

O carregador inicia um kernel contido na imagem. O Debian Live monta `filesystem.squashfs` e apresenta uma raiz overlay. Sem persistência, as alterações são temporárias; com o volume `blue-data`, a camada gravável fica nesse disco.

O Blue usa um único sistema compactado para que o funcionamento com persistência não dependa da prioridade entre módulos adicionais. Mudanças no disco persistente podem sobrepor arquivos da ISO; trocar a ISO não garante a substituição de todas as configurações já salvas.

## Desktop

LXDE fornece a sessão e o painel, Openbox gerencia as janelas e PCManFM fornece a área de trabalho e o gerenciador de arquivos. A configuração Blue conserva uma barra inferior e a Lixeira no desktop. O tema é aplicado inicialmente preservando os atalhos do gerenciador de janelas.

## Vídeo em VM

O serviço `blue-vbox` executa VBoxService. O autostart `blue-vm-display` inicia VBoxClient para VMSVGA na sessão do usuário. A regra udev dá ao grupo `video` acesso à interface `vboxuser` com modo 0660. O dispositivo privilegiado `vboxguest` permanece restrito.

## Assistente

O assistente é um programa Python com interface Tk. Lê métricas de `/proc`, uso do disco da pasta pessoal e classe X11 da janela ativa. O cliente de chat usa um endpoint fixo local e não executa respostas como comandos. Consulte [ASSISTENTE.md](../ASSISTENTE.md) e o [guia de privacidade](PRIVACIDADE.md).
