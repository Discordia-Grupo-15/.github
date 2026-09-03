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

Workflows: `ci-python.yml`, `ci-go.yml`, `ci-node.yml`, `secrets-scan.yml`.

Los status checks quedan como `ci / lint`, `ci / test`, `ci / build` y
`ci / secrets / gitleaks`.
