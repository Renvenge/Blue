# Usar o Blue em uma máquina virtual

## Configuração inicial

| Opção | Configuração usada nos testes |
| --- | --- |
| Tipo de sistema | Debian, Linux de 64 bits |
| Processadores | 2 |
| Memória | 2 GB |
| Vídeo | VMSVGA, 128 MB de memória de vídeo |
| Aceleração 3D | Desativada |
| Inicialização | UEFI, sem Secure Boot |
| Rede | NAT |
| Leitor óptico | ISO Blue 0.3 conectada |
| Disco de persistência | SATA, VDI de 32 GB, alocação dinâmica |

Esses valores são um ponto de partida para tarefas leves. Aumente a RAM conforme os aplicativos e projetos utilizados. O Blue não inclui um modelo de linguagem; sua execução pode exigir muito mais memória.

## Iniciar a sessão

Conecte a ISO e inicie a VM. Se o menu de boot aparecer, escolha a entrada Blue e pressione Enter. O desktop faz login automático como `blue`; o usuário Live tem acesso a sudo.

Quem recebeu a VM local já preparada deve iniciar **Blue**. Os nomes Blue-Test e Blue-Builder pertencem ao ambiente usado durante o desenvolvimento e não são necessários para usar a distribuição.

## Salvar arquivos e programas

O boot procura um sistema de arquivos ext4 com rótulo `blue-data`. Na raiz desse volume deve existir `persistence.conf` contendo:

```text
/ union
```

Esse volume fornece a camada gravável do sistema. A ISO continua sendo necessária: persistência não equivale a uma instalação convencional no disco.

Na VM local preparada, o volume já existe no arquivo `Blue-0.3-data.vdi`. Para criar outra VM persistente:

1. Crie um novo VDI vazio e conecte-o como disco SATA da VM.
2. Inicie uma sessão Linux e identifique esse disco com `lsblk -o PATH,TYPE,SIZE,MODEL,SERIAL,FSTYPE,MOUNTPOINTS`.
3. Execute o preparador abaixo com o caminho e o número de série exatos do disco criado.
4. Desligue e inicie novamente com a ISO Blue conectada.

```sh
# Substitua os dois valores pelos dados do NOVO disco vazio.
sudo python3 scripts/prepare-data-disk.py /dev/sdX --serial VB_NUMERO_DO_DISCO
```

O script cria partição e sistema de arquivos. Aceita apenas discos VirtualBox com modelo e série correspondentes e recusa partições, montagem, sistema de arquivos e assinaturas nos setores verificados. Ele foi usado em um disco recém-criado; não é um procedimento de recuperação nem uma garantia de que um disco antigo não tenha dados em outros setores. Não o use no disco do sistema de compilação ou em discos com arquivos.

Para conferir a persistência:

```sh
lsblk -o NAME,FSTYPE,LABEL,SIZE
findmnt -n -o SOURCE,FSTYPE,OPTIONS /
```

A raiz deve usar overlay com uma camada gravável em `/run/live/persistence/`. Crie um arquivo de teste, desligue pelo menu do Linux e ligue novamente para conferir seu conteúdo.

## Ajuste de tela

Com VMSVGA, habilite **Visualizar → Redimensionar automaticamente a tela do convidado** no VirtualBox. O cliente de vídeo inicia com a sessão LXDE e acompanha os pedidos de dimensão da janela. O assistente também adapta sua própria janela à resolução.

Se a barra inferior ficar fora da área visível, use temporariamente o modo escalonado no menu Visualizar e confira o controlador de vídeo. O menu do Blue também oferece ajuste manual de resolução.

Para investigar o cliente:

```sh
systemctl status blue-vbox
pgrep -a VBoxClient
ls -l /dev/vboxuser
xrandr --current
```

Na imagem atual, `/dev/vboxuser` usa o grupo `video` e modo 0660. A integração foi validada no VirtualBox 7.0.8; outras versões precisam ser testadas.

## Backup e desligamento

Desligue o Linux normalmente antes de fechar a VM. Com ela desligada, copie o VDI para preservar seus arquivos e programas. Uma cópia da ISO sozinha não contém os dados gravados no disco persistente.

Arquivos de outra VM não são migrados automaticamente. VMs, discos e backups pessoais não fazem parte do repositório público do Blue.
