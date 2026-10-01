# Contribuir com o Blue

Renvenge mantém a direção do projeto. Correções, documentação, testes e sugestões são bem-vindos. Preserve o objetivo de um ambiente simples e voltado à programação.

## Reportar um problema

Abra uma issue no repositório em que o Blue estiver publicado. Informe versão da ISO, ambiente de execução, passos para reproduzir, resultado esperado e resultado observado. Para problemas de tela, inclua versão do VirtualBox, controlador gráfico e resolução.

Anexe apenas os trechos de log necessários. Remova credenciais e informações pessoais. Para uma possível vulnerabilidade, siga [SECURITY.md](SECURITY.md).

## Propor uma mudança

Explique o problema que a alteração resolve. Em mudanças maiores, uma issue antes da implementação ajuda a combinar o escopo. Abra um pull request com a mudança e as verificações realizadas.

Use nomes claros, funções com responsabilidade definida e comentários que expliquem decisões. Não adicione serviços ao iniciar a sessão, downloads automáticos ou coleta de dados sem documentar o comportamento e discutir sua necessidade.

## Verificar

```sh
python3 -m unittest discover -s assistant -v
python3 -m unittest discover -s tests -v
```

Mudanças na imagem exigem compilação e teste em VM. Mudanças no desktop exigem captura da tela; mudanças em persistência exigem desligar e ligar novamente. Documentação deve manter links válidos e distinguir resultados medidos de expectativas.

Não envie ISOs, VDIs, diretórios de construção, credenciais ou ambientes pessoais em pull requests. Preserve os avisos de licença e os créditos. Mantenha as discussões respeitosas e centradas no trabalho.
