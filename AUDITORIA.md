# Auditoria tecnica do Axiel PDF

Data da auditoria: 2026-04-24  
Diretorio auditado: `E:\pdf\pdf_merger`

Atualizacao arquitetural: a partir da versao `1.6`, o projeto passou a ter camadas globais `app/`, `modules/`, `integrations/` e `ui/components/`. A pasta vazia acidental `{ui,core,assets}` foi removida. A auditoria historica abaixo deve ser lida junto com o `CHANGELOG.md` e o codigo real atual.

## Resumo executivo

O Axiel PDF e um aplicativo desktop Python/PyQt6 para combinar arquivos PDF. A arquitetura e simples e local: a interface grafica coleta arquivos, mantem a ordem dos documentos, exibe preview da primeira pagina e delega o merge para uma thread de trabalho.

Nao existe backend web, API HTTP, banco de dados, autenticacao, filas externas ou rotas. Neste projeto, o equivalente a "rotas" sao os fluxos de eventos da UI e os sinais PyQt que conectam tela, lista, preview e workers.

## Arvore real

```text
pdf_merger/
|-- main.py
|-- requirements.txt
|-- build.sh
|-- README.md
|-- AUDITORIA.md
|-- AGENTS.md
|-- core/
|   |-- pdf_engine.py
|   |-- pdf_item.py
|   `-- workers.py
|-- ui/
|   |-- main_window.py
|   |-- pdf_list.py
|   `-- preview_panel.py
`-- {ui,core,assets}/
```

Observacoes:

- A pasta `{ui,core,assets}` existe fisicamente, mas esta vazia. Ela parece ter sido criada por engano a partir de uma tentativa de brace expansion que nao funciona no PowerShell.
- Existem pastas `__pycache__` geradas automaticamente pelo Python. Elas nao fazem parte da arquitetura fonte.
- Nao ha arquivos locais de regras existentes antes desta auditoria: `AGENTS.md`, `.windsurf/rules/` e `CLAUDE.md` nao existiam.

## Stack identificada

Dependencias declaradas em `requirements.txt`:

- `PyQt6>=6.6.0`: interface desktop.
- `pymupdf>=1.23.0`: leitura de PDFs, contagem de paginas e renderizacao de thumbnails via `fitz`.
- `pikepdf>=8.0.0`: merge de PDFs via qpdf.

Ferramenta de build:

- `PyInstaller`, instalado pelo proprio `build.sh`.

## Entrada da aplicacao

Arquivo: `main.py`

Responsabilidades:

- Ajusta `sys.path` para permitir imports locais ao rodar como script ou executavel.
- Configura politica HiDPI do Qt.
- Cria `QApplication`.
- Define nome da aplicacao e organizacao.
- Define fonte padrao.
- Instancia e exibe `MainWindow`.
- Entra no loop de eventos com `app.exec()`.

Fluxo:

```text
python main.py
  -> QApplication
  -> MainWindow()
  -> window.show()
  -> app.exec()
```

## Arquitetura

O projeto esta dividido em duas camadas principais.

### Camada `ui/`

Responsavel por interface grafica, interacao com usuario, estado visual e orquestracao de alto nivel.

- `ui/main_window.py`: janela principal, topbar, bottombar, botoes, status, progresso e orquestracao de merge.
- `ui/pdf_list.py`: lista de PDFs, selecao, remocao, renomeacao, reorder por botoes e drag and drop externo.
- `ui/preview_panel.py`: painel lateral de preview e dados do PDF selecionado.

### Camada `core/`

Responsavel por modelo simples, operacoes com PDFs e workers.

- `core/pdf_item.py`: dataclass `PdfItem` com caminho, rotulo, paginas e tamanho.
- `core/pdf_engine.py`: funcoes puras/operacionais para thumbnail, contagem de paginas, tamanho e merge.
- `core/workers.py`: `QThread`s para thumbnail e merge, evitando travar a UI durante operacoes longas.

## Fluxo funcional principal

### 1. Adicionar PDFs por botao

```text
MainWindow._add_files()
  -> QFileDialog.getOpenFileNames()
  -> para cada path:
       PdfItem(path)
       get_page_count(path)
       get_file_size_str(path)
  -> PdfListWidget.add_items(new_items)
  -> PdfListWidget.list_changed
  -> MainWindow._update_merge_btn()
  -> MainWindow._update_stats()
```

Regras atuais:

- Aceita apenas arquivos selecionados pelo filtro `Arquivos PDF (*.pdf)`.
- Evita duplicidade por caminho exato.
- O botao de merge so fica habilitado com 2 ou mais itens.

### 2. Adicionar PDFs por drag and drop

```text
PdfListWidget.dragEnterEvent()
  -> aceita se houver URLs

PdfListWidget.dropEvent()
  -> filtra arquivos cujo caminho termina com .pdf
  -> cria PdfItem
  -> carrega paginas e tamanho
  -> add_items()
  -> list_changed
```

Observacao: o status inferior da janela nao e atualizado diretamente no drop, mas estatisticas e botao de merge sao atualizados via sinal `list_changed`.

### 3. Selecionar PDF e gerar preview

```text
PdfListWidget._select(index)
  -> selection_changed.emit(PdfItem)
  -> MainWindow._on_selection(item)
  -> PreviewPanel.show_item(item)
  -> ThumbnailWorker.start()
  -> get_thumbnail(path)
  -> thumbnail_ready
  -> PreviewPanel._on_thumbnail()
```

O preview renderiza a primeira pagina do PDF e mostra:

- nome exibido;
- numero de paginas;
- tamanho do arquivo.

### 4. Renomear item

```text
PdfRowWidget.start_edit()
  -> troca QLabel por QLineEdit
  -> usuario edita
  -> _finish_edit()
  -> atualiza PdfItem.label e label visual
```

Importante: a renomeacao e apenas o rotulo exibido na interface. Ela nao renomeia o arquivo no disco e nao altera o nome das paginas no PDF final.

### 5. Reordenar PDFs

```text
_move_up()
_move_down()
_move_top()
_move_bottom()
  -> reorganizam self.items
  -> _rebuild()
  -> list_changed
```

O README menciona drag and drop interno para reordenar, mas o codigo atual implementa apenas os botoes de movimentacao. O drag and drop implementado e para entrada de arquivos externos.

### 6. Remover e limpar

Remover um item:

```text
PdfRowWidget.btn_remove
  -> remove_requested(index)
  -> PdfListWidget.remove_item(index)
  -> _rebuild()
  -> list_changed
```

Limpar tudo:

```text
MainWindow._clear_all()
  -> QMessageBox.question()
  -> PdfListWidget.clear_all()
  -> selection_changed(None)
  -> _update_stats()
```

### 7. Juntar PDFs

```text
MainWindow._merge()
  -> pdf_list.get_paths()
  -> QFileDialog.getSaveFileName()
  -> desabilita botoes
  -> mostra progresso
  -> MergeWorker(paths, out).start()

MergeWorker.run()
  -> merge_pdfs(paths, output, progress.emit)

merge_pdfs()
  -> pikepdf.Pdf.new()
  -> para cada path:
       pikepdf.open(path)
       writer.pages.extend(src.pages)
  -> writer.save(output_path)
  -> retorna True/False

MainWindow._on_merge_done()
  -> reabilita UI
  -> mostra sucesso/erro
  -> opcionalmente abre arquivo gerado
```

## Rotas

Nao ha rotas HTTP neste projeto.

Mapa equivalente de eventos e handlers:

| Acao do usuario | Handler principal | Modulo |
|---|---|---|
| Abrir app | `main()` | `main.py` |
| Adicionar PDFs por dialogo | `MainWindow._add_files()` | `ui/main_window.py` |
| Adicionar PDFs por drop | `PdfListWidget.dropEvent()` | `ui/pdf_list.py` |
| Selecionar item | `PdfListWidget._select()` | `ui/pdf_list.py` |
| Atualizar preview | `PreviewPanel.show_item()` | `ui/preview_panel.py` |
| Renomear item | `PdfRowWidget.start_edit()` / `_finish_edit()` | `ui/pdf_list.py` |
| Remover item | `PdfListWidget.remove_item()` | `ui/pdf_list.py` |
| Limpar lista | `MainWindow._clear_all()` | `ui/main_window.py` |
| Reordenar | `_move_up`, `_move_down`, `_move_top`, `_move_bottom` | `ui/pdf_list.py` |
| Juntar PDFs | `MainWindow._merge()` | `ui/main_window.py` |
| Executar merge | `MergeWorker.run()` / `merge_pdfs()` | `core/workers.py`, `core/pdf_engine.py` |

## Tela e componentes

### Janela principal

Arquivo: `ui/main_window.py`

Layout:

- Topbar fixa com logo, badge `PRO`, contadores e botoes.
- Corpo com lista de PDFs no centro/esquerda.
- Divisor vertical.
- Painel de preview lateral direito.
- Bottombar com status e barra de progresso.

### Lista de PDFs

Arquivo: `ui/pdf_list.py`

Estados:

- Vazio: drop zone com texto para arrastar PDFs.
- Com itens: scroll area com linhas customizadas.

Cada linha possui:

- indice;
- icone textual;
- nome/rotulo;
- metadados de paginas e tamanho;
- botao de renomear;
- botao de remover.

### Preview

Arquivo: `ui/preview_panel.py`

Estados:

- Sem selecao: placeholder.
- Carregando: label `Carregando...`.
- Carregado: thumbnail da primeira pagina e metadados.

## Funcionalidades implementadas

- Adicionar PDFs por seletor de arquivos.
- Adicionar PDFs por drag and drop externo.
- Evitar duplicidade por caminho exato.
- Contar paginas.
- Exibir tamanho formatado.
- Exibir estatisticas de quantidade e paginas totais.
- Selecionar PDF na lista.
- Preview da primeira pagina.
- Renomear rotulo visual.
- Remover item individual.
- Limpar lista com confirmacao.
- Reordenar por botoes: subir, descer, inicio e final.
- Gerar PDF combinado com progresso.
- Abrir arquivo gerado apos sucesso.
- Build empacotado via PyInstaller.

## Lacunas e divergencias

1. O README afirma reordenacao por drag and drop interno, mas o codigo nao implementa esse recurso.
2. O README e os comentarios exibem caracteres corrompidos, indicando problema de encoding em algum momento da criacao/edicao dos arquivos.
3. `merge_pdfs()` ignora PDFs que falham individualmente e ainda pode retornar sucesso se pelo menos o salvamento final ocorrer. Isso pode gerar um PDF incompleto sem erro claro para o usuario.
4. Se todos os PDFs falharem ao abrir, o fluxo ainda tenta salvar um PDF vazio.
5. `get_page_count()` captura excecao sem registrar erro; isso dificulta diagnostico.
6. `get_file_size_str()` nao trata excecoes; caminho inacessivel pode quebrar o carregamento.
7. A duplicidade usa caminho exato e pode nao detectar diferencas de caixa/caminho normalizado em alguns sistemas.
8. O build script usa `--add-data "ui:ui"` e `--add-data "core:core"`, formato adequado para Linux/macOS. No PyInstaller nativo Windows, o separador esperado costuma ser `;`.
9. Nao ha testes automatizados.
10. A pasta vazia `{ui,core,assets}` deve ser removida ou explicada, pois nao participa da aplicacao.

## Riscos tecnicos

| Risco | Impacto | Local |
|---|---|---|
| Merge silenciosamente incompleto | Usuario acredita que todos os PDFs foram unidos quando alguns foram pulados | `core/pdf_engine.py` |
| Falhas de arquivo sem feedback detalhado | Diagnostico ruim em PDFs bloqueados/corrompidos | `core/pdf_engine.py`, `ui/main_window.py` |
| README divergente do codigo | Expectativa incorreta sobre drag and drop de ordenacao | `README.md`, `ui/pdf_list.py` |
| Encoding corrompido | UI e documentacao podem aparecer com caracteres estranhos | varios arquivos |
| Build Windows inconsistente | `build.sh` pode falhar fora de Git Bash/WSL ou com separador errado do PyInstaller | `build.sh` |
| Sem testes | Regressao manual em fluxos de UI e merge | projeto inteiro |

## Validacao realizada

Comando executado:

```powershell
python -m compileall -q .
```

Resultado: sintaxe Python valida no estado auditado.

## Recomendacoes priorizadas

1. Corrigir encoding dos arquivos fonte e README para UTF-8 limpo.
2. Ajustar `merge_pdfs()` para retornar erro quando algum PDF falhar, ou ao menos reportar lista de arquivos ignorados.
3. Validar que o output contem paginas antes de mostrar sucesso.
4. Tratar excecoes em `get_file_size_str()` e registrar falhas em `get_page_count()`.
5. Implementar de fato reordenacao por drag and drop interno ou remover essa promessa do README.
6. Remover a pasta vazia `{ui,core,assets}` se nao houver uso planejado.
7. Criar testes pequenos para `PdfItem`, formatacao de tamanho e merge com PDFs de amostra.
8. Tornar o build multiplataforma explicito, com script separado para Windows ou deteccao de separador do PyInstaller.
