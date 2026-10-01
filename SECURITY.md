# Segurança

Blue 0.3 é uma versão experimental. Não há compromisso de suporte de longo prazo ou prazo definido para correções. Os pacotes Debian seguem seus próprios canais de atualização; o Blue não opera um repositório próprio de atualizações.

## Reportar uma vulnerabilidade

Se o repositório oferecer **Security → Report a vulnerability**, use esse canal privado. Inclua versão, passos mínimos de reprodução, impacto e arquivos envolvidos. Não publique credenciais, dados pessoais ou detalhes de exploração em uma issue aberta.

O canal privado precisa ser habilitado pelo mantenedor ao publicar o repositório. Se ele ainda não estiver disponível, abra uma issue solicitando um contato privado, sem expor o problema. Este projeto não declara endereço de e-mail ou canal externo de Renvenge.

## Comportamentos relevantes

- A sessão Live entra automaticamente como `blue`, com sudo. Não é uma configuração pensada para um computador público compartilhado.
- O disco persistente preparado pelo projeto não usa criptografia. Quem tem acesso ao VDI pode acessar os dados nele.
- O assistente roda como usuário comum, não executa respostas do modelo e utiliza um endpoint local fixo.
- A interface VirtualBox `vboxuser` é acessível ao grupo `video`; a interface privilegiada permanece restrita.

Consulte [PRIVACIDADE.md](docs/PRIVACIDADE.md) para a coleta do assistente. Testes em VM não constituem auditoria completa de segurança da distribuição.
