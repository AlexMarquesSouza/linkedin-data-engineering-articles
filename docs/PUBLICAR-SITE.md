# Publicar o site no GitHub Pages

O workflow `.github/workflows/pages.yml` valida os projetos, constrói o MkDocs e envia o HTML ao GitHub Pages após cada push para `main`.

## Primeira ativação manual

1. Abra [Settings → Pages](https://github.com/AlexMarquesSouza/linkedin-data-engineering-articles/settings/pages).
2. Em **Build and deployment → Source**, selecione **GitHub Actions**.
3. Volte ao repositório e abra a aba **Actions**.
4. Selecione **Publicar site no GitHub Pages**.
5. Use **Run workflow → main → Run workflow** caso o push não tenha iniciado automaticamente.
6. Aguarde os jobs `build` e `deploy` ficarem verdes.

URL esperada:

```text
https://alexmarquessouza.github.io/linkedin-data-engineering-articles/
```

## Publicação manual das alterações locais

Na pasta do repositório:

```bash
git status
git add .github/workflows/pages.yml docs/PUBLICAR-SITE.md mkdocs.yml
git commit -m "Configura publicacao do site no GitHub Pages"
git push origin main
```

## Diagnóstico

- Se `build` falhar, abra o log da etapa correspondente.
- Se `deploy` informar que Pages não está habilitado, repita a seleção **Source: GitHub Actions**.
- Se o site abrir sem estilos, confirme que `actions/configure-pages@v5` passou.
- O diretório `site-local` não deve ser enviado ao Git; o workflow sempre o recria.

Nenhuma credencial deve ser adicionada. O workflow usa somente o token temporário fornecido pelo GitHub Actions.

