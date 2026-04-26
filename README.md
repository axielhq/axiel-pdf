# Axiel PDF

**Automacao inteligente para PDFs em grande volume.**

O Axiel PDF e uma ferramenta criada para processar, organizar e unir arquivos PDF com apoio de automacao, OCR e IA.

O foco do projeto e reduzir trabalho manual em fluxos documentais. A base atual do aplicativo ja permite uniao local de PDFs, organizacao da lista e pre-visualizacao. Recursos de OCR, renomeacao inteligente, deteccao de duplicidade e analise textual fazem parte da evolucao planejada.

## Recursos atuais

- Uniao local de PDFs pela interface desktop
- Adicao de arquivos por seletor
- Adicao de arquivos por drag and drop externo
- Reordenacao por botoes
- Renomeacao visual do rotulo na lista
- Remocao de itens
- Pre-visualizacao da primeira pagina
- Visualizacao ampliada com zoom

## Recursos planejados

- OCR para extracao de texto
- Renomeacao inteligente com IA
- Deteccao de PDFs duplicados
- Identificacao de paginas em branco
- Extracao e analise de texto
- Validacao textual em fluxos documentais

## Uso profissional

O Axiel PDF pode servir como base para fluxos personalizados de empresas e profissionais que lidam com muitos documentos, como setores administrativos, juridico, contabilidade, RH, operacoes internas e arquivos digitais.

## Solucoes sob demanda

A Axiel pode desenvolver fluxos personalizados, integracoes e automacoes documentais conforme a necessidade de cada empresa ou profissional.

Para projetos comerciais, customizacoes ou parcerias, utilize o canal oficial informado no perfil da Axiel no GitHub.

## Status

Versao atual da aplicacao: `1.0.2`.

O projeto esta em desenvolvimento inicial. A interface atual e funcional para o fluxo principal de uniao de PDFs. OCR e IA aparecem na interface como capacidades planejadas e ainda nao executam processamento externo.

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

## Privacidade

O Axiel PDF trabalha com arquivos locais. Sempre revise logs, capturas de tela e exemplos antes de publicar qualquer material que possa expor caminhos, documentos ou dados pessoais.

## Sobre a Axiel

A Axiel cria ferramentas praticas, automacoes inteligentes e solucoes personalizadas para empresas e profissionais que precisam otimizar processos, organizar documentos, automatizar tarefas e aplicar IA no dia a dia.

Frase institucional:
Ferramentas, automacoes e solucoes com IA para fluxos reais de trabalho.

## Licenca

Este projeto usa a GNU General Public License v3.0. Consulte `LICENSE` para os termos completos.
