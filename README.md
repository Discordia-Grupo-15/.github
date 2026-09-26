# .github

Templates y reusable workflows de la organizacion.

Aca no se escriben URLs internas, nombres de buckets ni endpoints. Todo por variable
o secret.

## Uso

```yaml
jobs:
  ci:
    uses: Discordia-Grupo-15/.github/.github/workflows/ci-go.yml@main
```

Workflows: `ci-python.yml`, `ci-go.yml`, `ci-node.yml`, `build-image.yml`,
`secrets-scan.yml`.

Los workflows de CI corren lint, tests y el escaneo de secretos en un solo job,
asi que el status check queda como `ci / check`. GitHub redondea cada job al
minuto, y separarlos multiplicaba el consumo.

La imagen no se construye en el CI. En los pull requests la arma
`build-image.yml`, que cada repo llama desde un workflow propio filtrado por
`paths` a los archivos que cambian como se construye (Dockerfile, lockfiles):

```yaml
on:
  pull_request:
    paths: [Dockerfile, .dockerignore, uv.lock, pyproject.toml]

jobs:
  image:
    uses: Discordia-Grupo-15/.github/.github/workflows/build-image.yml@main
```

El escaneo de secretos tambien existe como action, para usarlo como paso:

```yaml
- uses: Discordia-Grupo-15/.github/.github/actions/gitleaks@main
```
