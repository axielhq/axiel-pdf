# Axiel PDF

**Automacao inteligente para PDFs em grande volume.**

Aplicativo desktop para unir, organizar e visualizar arquivos PDF com foco em fluxos documentais reais. O projeto foi criado para reduzir trabalho manual em operacoes que lidam com muitos arquivos e precisa manter processamento local como base do fluxo.

O estado atual do sistema cobre bem a etapa principal de uniao de PDFs. Recursos como OCR, renomeacao inteligente, deteccao de duplicidade e analise textual fazem parte da evolucao planejada e ainda nao estao entregues no fluxo operacional.

## Visao geral

- Aplicativo local em Python com interface PyQt6
- Fluxo atual focado em uniao e organizacao de PDFs
- Pre-visualizacao da primeira pagina antes do merge
- Base preparada para evolucao com OCR e automacoes documentais
- Projeto mantido pela Axiel como ferramenta pratica para produtividade documental

## Navegacao rapida

- [Recursos atuais](#recursos-atuais)
- [Recursos em evolucao](#recursos-em-evolucao)
- [Uso profissional](#uso-profissional)
- [Instalacao](#instalacao)
- [Como rodar](#como-rodar)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Privacidade](#privacidade)
- [Sobre a Axiel](#sobre-a-axiel)

## Onde o Axiel PDF ajuda

O Axiel PDF faz sentido em ambientes que precisam lidar com grande volume de documentos, consolidacao de arquivos e conferencias rapidas antes de gerar um PDF final.

Exemplos de uso:

- setores administrativos
- escritorio juridico
- contabilidade
- RH
- operacoes internas
- arquivos digitais
- fluxos documentais personalizados

## Recursos atuais

- Uniao local de PDFs pela interface desktop
- Adicao de arquivos por seletor
- Adicao de arquivos por drag and drop externo
- Reordenacao por botoes
- Renomeacao visual do rotulo na lista
- Remocao de itens
- Pre-visualizacao da primeira pagina
- Visualizacao ampliada com zoom
- Tela inicial institucional e secao sobre

## Recursos em evolucao

Os itens abaixo fazem parte da direcao do produto, mas nao devem ser tratados como recursos entregues no estado atual:

- OCR para extracao de texto
- Renomeacao inteligente com IA
- Deteccao de PDFs duplicados
- Identificacao de paginas em branco
- Extracao e analise de texto
- Validacao textual em fluxos documentais

## Uso profissional

O Axiel PDF pode servir como base para fluxos personalizados de empresas e profissionais que precisam organizar documentos, unir arquivos em lote e preparar uma esteira documental mais eficiente.

Ele tambem pode funcionar como ponto de partida para automacoes maiores envolvendo OCR, classificacao documental, organizacao de arquivos e integracoes sob demanda.

## Status

Versao atual da aplicacao: `1.0.2`

Estado do projeto:

- funcional para o fluxo principal de uniao de PDFs
- interface desktop pronta para uso local
- OCR e IA presentes apenas como direcao de evolucao

## Requisitos

- Python 3.11 ou superior
- Dependencias listadas em `requirements.txt`

## Instalacao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Como rodar

```powershell
python main.py
```

## Build

O script `build.sh` usa PyInstaller para gerar um executavel desktop:

```bash
./build.sh
```

O executavel e criado em `dist/`.

## Estrutura do projeto

```text
app/           bootstrap, paths, configuracao e versao
core/          leitura, preview e uniao de PDFs
ui/            interface PyQt6
ui/components/ componentes reutilizaveis
modules/       manifestos de recursos atuais e planejados
integrations/  registro de provedores planejados
assets/        imagens e icones
```

## Solucoes sob demanda

A Axiel pode desenvolver fluxos personalizados, integracoes e automacoes documentais conforme a necessidade de cada empresa ou profissional.

Para projetos comerciais, customizacoes ou parcerias, utilize o canal oficial informado no perfil da Axiel no GitHub.

## Privacidade

O Axiel PDF trabalha com arquivos locais. Sempre revise logs, capturas de tela e exemplos antes de publicar qualquer material que possa expor caminhos, documentos ou dados pessoais.

## Sobre a Axiel

A Axiel cria ferramentas praticas, automacoes inteligentes e solucoes personalizadas para empresas e profissionais que precisam otimizar processos, organizar documentos, automatizar tarefas e aplicar IA no dia a dia.

**Ferramentas, automacoes e solucoes com IA para fluxos reais de trabalho.**

## Licenca

Este projeto usa a GNU General Public License v3.0. Consulte `LICENSE` para os termos completos.
