# Symbols Studio

Arquivo visual independente de símbolos gráficos, baseado no *Symbol Sourcebook: An Authoritative Guide to International Graphic Symbols*, de Henry Dreyfuss (McGraw-Hill, 1972).

## O que o site contém hoje

- **15 redesenhos vetoriais esquemáticos** na coleção de estudos originais.\n- **118 símbolos vetorizados em SVG** das páginas impressas 34–36, com ficheiros individuais e referência de origem.
- **1.825 entradas textuais do índice impresso**, com nomes e referências de páginas extraídos do PDF fornecido.
- Uma aba **All sourcebook plates · local PDF** permite abrir as pranchas ilustradas no navegador. O PDF é selecionado localmente, sem ser enviado ao site. A galeria navega pelas páginas 26–247 do arquivo.
- A interface separa **Visual symbols**, **Book index · text only** e a visualização local do PDF. A página inicial agora abre diretamente na coleção visual e oferece download de SVG individual nas fichas.
- O site ainda não tem cada símbolo separado em uma ficha vetorial própria. Para acessar os desenhos reais já existentes no livro, use o visualizador local das pranchas. A transformação do restante das pranchas em fichas individuais exige extração, redesenho e conferência símbolo por símbolo.

A extração automática do índice pode conter erros de OCR. Confira a página citada no PDF antes de usar uma referência em publicação acadêmica ou comercial. Os 118 SVGs das páginas 34–36 são vetorização automatizada inicial e podem conter imperfeições nos contornos.

## SVGs individuais

O catálogo compactado em `data/symbols-page34.json.gz`, `data/symbols-page35.json.gz` e `data/symbols-page36.json.gz` armazena cada desenho como SVG independente. O workflow usa `scripts/export_svg_catalog.py` para gerar arquivos `.svg` individuais e um ZIP de download durante a publicação. A primeira leva contém 118 símbolos das páginas impressas 34–36; isso não equivale ainda ao conteúdo visual completo do livro.\n\n## Publicação no GitHub Pages

O workflow em `.github/workflows/pages.yml` publica os arquivos estáticos a cada push para `main`. Em **Settings → Pages**, mantenha Source como **GitHub Actions**.

URL: https://studio-gh.github.io/symbols-studio/

## Fonte e atribuição

Dreyfuss, Henry. *Symbol Sourcebook: An Authoritative Guide to International Graphic Symbols*. New York: McGraw-Hill, 1972.

As fichas visuais são redesenhos esquemáticos originais, não scans nem fac-símiles das pranchas. Crédito bibliográfico não substitui autorização de reprodução. O índice textual serve como ferramenta de localização, não como substituto do catálogo visual.
