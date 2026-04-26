# Changelog

As mudancas importantes do Axiel PDF sao documentadas neste arquivo.

## [Unreleased]

### Documentacao

- Ajuste do posicionamento da marca Axiel em portugues brasileiro.
- Revisao do README, contribuicao, seguranca e roadmap para alinhar o repositorio como vitrine profissional.
- Reestruturacao do README do Axiel PDF para uma apresentacao mais forte no GitHub, com abertura, navegacao rapida e separacao mais clara entre recursos atuais e evolucao planejada.
- Refinada a apresentacao do README com titulo mais forte, badges tecnicas, links rapidos e secoes em estilo vitrine adaptadas ao Axiel PDF.

## [1.0.2] - 2026-04-26

### Alterado

- Definida a versao publica da aplicacao como `1.0.2`.
- Adicionado o codigo-fonte atual da aplicacao desktop em PyQt6.
- Adicionadas a tela inicial, a secao sobre e o rodape institucional.
- Adicionados os assets visuais atuais do projeto.
- Adicionados `LICENSE`, `README.md` e `.gitignore`.

## Historico local de implementacao

As entradas abaixo registram a evolucao local da aplicacao antes da primeira publicacao do codigo-fonte no GitHub.

### Versao 2.8 - Rodape institucional

- Adicionado texto discreto de copyright e GPLv3 no rodape da janela principal.

### Versao 2.7 - Tela inicial

- Adicionada tela inicial modal exibida na abertura do aplicativo.
- Adicionado o logo do Axiel PDF como asset local.
- Adicionado o botao `Entrar` antes da janela principal.

### Versao 2.6 - Secao Sobre

- Adicionado o botao `Sobre` na barra superior.
- Adicionado modal com descricao do produto, autoria da Axiel, licenca GNU GPL v3.0, versao e link do GitHub.

### Versao 2.5 - Limpeza visual da lista

- Removido o fundo em caixa ao redor dos textos de nome e metadados.
- Mantidas as faixas zebra por linha.

### Versao 2.4 - Lista zebra sem grade

- Removidas as linhas internas verticais e horizontais da lista.
- Mantidos os estados de selecao e destaque de movimentacao.

### Versao 2.3 - Reconstrucao da lista

- Reestruturado o layout da lista com colunas fixas.
- Alinhadas as informacoes de documentos e acoes.
- Aplicada visualizacao continua em zebra.

### Versao 2.2 - Aplicacao das cores da lista

- Corrigida a aplicacao visual do fundo das linhas.
- Melhorado o contraste entre linhas alternadas.

### Versao 2.1 - Lista continua

- Ajustado o layout para uma lista continua.
- Removido o espacamento tipo card entre documentos.

### Versao 2.0 - Separacao horizontal

- Melhorada a separacao visual entre linhas.
- Mantidos os destaques de selecao e movimentacao.

### Versao 1.9 - Lista em grade leve

- Adicionado cabecalho visual de colunas.
- Aplicadas linhas alternadas com contraste leve.

### Versao 1.8 - Lista mais legivel

- Adicionado icone de PDF em cada linha.
- Adicionado destaque temporario para item movido.

### Versao 1.7 - Preview ampliado

- Adicionado popup de visualizacao ampliada.
- Adicionados scroll e controles de zoom.

### Versao 1.6 - Fundacao modular

- Adicionados `app/`, `modules/`, `integrations/` e `ui/components/`.
- Centralizada a resolucao de assets.
- Movida a identidade e a versao para `app.version`.
- Preparada a leitura de credenciais por variaveis de ambiente.

### Versao 1.5 - Preparacao para IA e OCR

- Adicionados manifestos de capacidades futuras de IA e OCR.
- Adicionados provedores planejados e variaveis de ambiente relacionadas.
- Adicionadas entradas de interface para IA e OCR como recursos planejados.

### Versao 1.4 - Icone no botao de adicionar

- Adicionado o icone de PDF ao botao `Adicionar PDFs`.

### Versao 1.3 - Identidade visual do PDF

- Adicionado `assets/pdf_badge.svg`.
- Atualizados os assets de identidade visual.
- Atualizado o empacotamento de assets no build.

### Versao 1.2 - Interface mais limpa

- Removidos icones decorativos de partes da interface.
- Simplificados os rotulos de acoes.

### Versao 1.1 - Identidade Axiel PDF

- Definido o nome oficial `Axiel PDF`.
- Atualizados o titulo da aplicacao, a organizacao e o nome padrao do PDF combinado.

### Versao 1.0 - Base auditada

- Aplicativo desktop PyQt6 para juntar PDFs.
- Adicao, remocao, renomeacao visual e ordenacao por botoes.
- Preview da primeira pagina.
- Contagem de paginas e tamanho de arquivo.
- Merge por `pikepdf` em worker separado.
- Barra de progresso durante o merge.
