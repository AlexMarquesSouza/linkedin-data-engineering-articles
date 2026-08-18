from pathlib import Path

root=Path(__file__).resolve().parents[1]
header='''site_name: LinkedIn — Notícias técnicas com implementação
site_description: Artigos de Engenharia de Dados acompanhados de código local e testes
use_directory_urls: false
docs_dir: .
site_dir: ../site-local/linkedin
theme:
  name: material
  language: pt-BR
  features:
    - navigation.sections
    - navigation.top
    - content.code.copy
  palette:
    primary: blue
    accent: light blue
markdown_extensions:
  - admonition
  - attr_list
  - toc:
      permalink: true
exclude_docs: |
  **/__pycache__/**
  **/data/**
  **/src/**
  **/tests/**
  scripts/**
  mkdocs.yml
nav:
  - Início: README.md
  - Padrão didático: docs/PADRAO-DIDATICO.md
  - 000 — Configuração: 000-configuracao-ambiente/README.md
'''
lines=[header.rstrip()]
for folder in sorted(root.glob('[0-9][0-9][0-9][0-9]-*')):
    title=(folder/'README.md').read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
    lines.extend([f"  - '{folder.name[:4]} — {title.replace(chr(39), chr(39)*2)}':",f"      - Tutorial: {folder.name}/README.md",f"      - Artigo recuperado: {folder.name}/artigo-linkedin.md",f"      - Post com implementação: {folder.name}/post-linkedin.md"])
(root/'mkdocs.yml').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Navegação do site LinkedIn atualizada.')
