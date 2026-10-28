# Symbols Studio

Arquivo visual independente de símbolos gráficos, inspirado na estrutura de consulta do *Symbol Sourcebook* de Henry Dreyfuss.

## Publicação no GitHub Pages
1. Crie um repositório público chamado `symbols-studio` na conta `studio-gh`.
2. Envie o conteúdo desta pasta para a branch `main`.
3. Em **Settings → Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)`. Salve.
4. O site deverá ficar disponível em `https://studio-gh.github.io/symbols-studio/`.

O workflow em `.github/workflows/pages.yml` também pode publicar pelo GitHub Actions se a opção de Pages estiver configurada para GitHub Actions.

## Conteúdo e atribuição
Cada registro em `data/symbols.json` tem um objeto `source` com autor, título, editora, ano, página e nota de crédito. O site usa descrições editoriais em português, não transcrições do livro. As formas SVG desta primeira versão são redesenhos esquemáticos originais para demonstrar a interface, não reproduções fac-similares das pranchas.

Referência: Dreyfuss, Henry. *Symbol Sourcebook: An Authoritative Guide to International Graphic Symbols*. New York: McGraw-Hill, 1972.

## Estado do catálogo
A primeira versão inclui uma seleção demonstrativa dos símbolos básicos listados no livro. A paginação deve ser conferida contra a edição usada antes de ampliar o catálogo. Não inclua scans, reproduções extensas ou desenhos protegidos sem verificar os direitos de uso.
