# Instrucoes para agentes no projeto Axiel PDF

## Prioridade de contexto

Ao trabalhar neste diretorio, siga esta ordem:

1. `AGENTS.md`
2. `AUDITORIA.md`
3. `README.md`
4. Codigo real em `main.py`, `core/` e `ui/`

Se houver conflito entre respostas anteriores, conhecimento generico e arquivos locais, siga os arquivos locais e o codigo real.

## Identidade do projeto

Este projeto e um aplicativo desktop local chamado Axiel PDF para juntar PDFs.

Nao trate este diretorio como:

- aplicacao web;
- API FastAPI;
- chatbot;
- projeto Central do Eletricista;
- sistema com PostgreSQL, Redis, Celery/RQ ou Next.js.

As instrucoes globais sobre Central do Eletricista nao se aplicam a este workspace, exceto como regra geral de nao inventar arquitetura e respeitar arquivos locais.

## Stack real

- Python
- PyQt6
- pymupdf / `fitz`
- pikepdf
- PyInstaller via `build.sh`

## Arquitetura real

- `app/bootstrap.py`: inicializacao do QApplication.
- `app/config.py`: leitura centralizada de configuracoes e credenciais.
- `app/paths.py`: resolucao de caminhos locais e empacotados.
- `app/version.py`: nome, organizacao e versao do produto.
- `main.py`: ponto de entrada da aplicacao.
- `modules/`: manifestos e capacidades funcionais por modulo.
- `integrations/`: registros de provedores externos planejados.
- `ui/main_window.py`: janela principal e orquestracao dos fluxos.
- `ui/components/`: componentes reutilizaveis da interface.
- `ui/components/pdf_preview_dialog.py`: visualizacao ampliada de preview com zoom e scroll.
- `ui/pdf_list.py`: lista de PDFs, selecao, remocao, renomeacao e ordenacao por botoes.
- `ui/preview_panel.py`: preview lateral em thread.
- `core/pdf_item.py`: modelo de dado `PdfItem`.
- `core/pdf_engine.py`: contagem, tamanho, thumbnail e merge.
- `core/workers.py`: workers PyQt para thumbnail e merge.

Nao crie estrutura paralela sem necessidade.

## Regras de trabalho

- Antes de alterar codigo, leia o arquivo real da area alvo.
- Prefira mudancas pequenas e coerentes com o estilo atual.
- Nao invente requisitos, telas, rotas HTTP ou backend.
- Documente divergencias entre README e codigo quando encontrar.
- Preserve a natureza desktop PyQt6 do projeto.
- Ao mexer em fluxo de PDF, valide comportamento de sucesso e erro.
- Ao alterar arquivos, releia os arquivos alterados antes de afirmar conclusao.
- Mantenha codigo limpo, direto e profissional, sem marcas, comentarios ou textos que indiquem geracao por IA.
- Nao deixe codigo morto, duplicado, experimental ou vestigios de tentativas anteriores.
- Cada implementacao funcional deve atualizar a versao do projeto em +0.1.
- Cada implementacao funcional deve ser registrada em `CHANGELOG.md`.
- A versao base auditada do sistema e `1.0`.
- Mudancas apenas documentais ou de processo nao alteram a versao, salvo instrucao explicita.

## Processo profissional obrigatorio

Para cada implementacao funcional:

1. Confirmar objetivo da mudanca.
2. Ler os arquivos reais da area afetada.
3. Listar fases, arquivos afetados, riscos e perguntas nao resolvidas quando a tarefa for media ou grande.
4. Implementar mantendo o desenho atual do projeto.
5. Remover qualquer codigo temporario, morto ou de debug.
6. Atualizar `CHANGELOG.md` com a nova versao.
7. Rodar validacao minima.
8. Reler os arquivos alterados antes de concluir.

## Validacao minima

Para mudancas Python, rode ao menos:

```powershell
python -m compileall -q .
```

Para mudancas de UI, quando possivel, execute manualmente:

```powershell
python main.py
```

## Estado conhecido em 2026-04-25

- Versao atual registrada: `2.3`.
- Nao existem rotas HTTP.
- Nao existem testes automatizados.
- O README menciona reordenacao por drag and drop interno, mas o codigo atual so implementa reordenacao por botoes.
- Ha caracteres corrompidos em README e comentarios/textos de UI.
- `merge_pdfs()` pode ignorar PDFs com erro e ainda retornar sucesso.
