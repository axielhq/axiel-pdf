<p align="center">
  <img src="assets/axiel_pdf_banner.png" alt="Axiel PDF" width="100%">
</p>

# Axiel PDF v1.0.2

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-Desktop-41CD52?style=flat-square&logo=qt&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-Preview-orange?style=flat-square)
![pikepdf](https://img.shields.io/badge/pikepdf-Merge-4B5563?style=flat-square)
![GPLv3](https://img.shields.io/badge/License-GPLv3-blue?style=flat-square)

**Automacao inteligente para PDFs em grande volume.**

Aplicativo desktop para unir, organizar e visualizar arquivos PDF com foco em fluxos documentais reais.

[Recursos atuais](#recursos-atuais) • [Destaques da versao atual](#destaques-da-versao-atual) • [Instalacao](#instalacao) • [Documentacao](#documentacao) • [Privacidade](#privacidade)

---

## Destaques da versao atual

- ✅ Uniao local de PDFs pela interface desktop
- ✅ Organizacao de arquivos com reordenacao por botoes
- ✅ Pre-visualizacao da primeira pagina antes do merge
- ✅ Visualizacao ampliada com zoom
- ✅ Fluxo local sem dependencia de servico web

## Sobre o projeto

O Axiel PDF foi criado para reduzir trabalho manual em operacoes que lidam com muitos documentos. O foco atual do sistema e consolidar arquivos PDF com rapidez, organizar a fila de arquivos e permitir uma conferencia basica antes da geracao final.

Recursos como OCR, renomeacao inteligente, deteccao de duplicidade e analise textual fazem parte da direcao do produto, mas ainda nao estao entregues no fluxo operacional.

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

Os itens abaixo fazem parte da evolucao planejada do projeto:

- OCR para extracao de texto
- Renomeacao inteligente com IA
- Deteccao de PDFs duplicados
- Identificacao de paginas em branco
- Extracao e analise de texto
- Validacao textual em fluxos documentais

## Uso profissional

Pode fazer sentido em operacoes como:

- setores administrativos
- escritorio juridico
- contabilidade
- RH
- operacoes internas
- arquivos digitais
- fluxos documentais personalizados

Tambem pode servir como base para fluxos maiores de organizacao documental, OCR e automacoes sob demanda.

## Solucoes sob demanda

A Axiel pode desenvolver customizacoes, integracoes e automacoes documentais a partir desta base, conforme a necessidade de cada empresa ou profissional.

Para projetos comerciais, customizacoes ou parcerias, utilize o canal oficial informado no perfil da Axiel no GitHub.

## Status

Versao atual da aplicacao: `1.0.2`

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

## Documentacao

- [CHANGELOG.md](CHANGELOG.md) - historico de mudancas
- [ROADMAP.md](ROADMAP.md) - direcao planejada do produto
- [CONTRIBUTING.md](CONTRIBUTING.md) - contribuicoes e padroes basicos
- [SECURITY.md](SECURITY.md) - reporte responsavel de problemas
- [AUDITORIA.md](AUDITORIA.md) - contexto tecnico e operacional do projeto

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

## Privacidade

O Axiel PDF trabalha com arquivos locais. Sempre revise logs, capturas de tela e exemplos antes de publicar qualquer material que possa expor caminhos, documentos ou dados pessoais.

## Sobre a Axiel

A Axiel cria ferramentas praticas, automacoes inteligentes e solucoes personalizadas para empresas e profissionais que precisam otimizar processos, organizar documentos, automatizar tarefas e aplicar IA no dia a dia.

**Ferramentas, automacoes e solucoes com IA para fluxos reais de trabalho.**

## Licenca

Este projeto usa a GNU General Public License v3.0. Consulte `LICENSE` para os termos completos.
