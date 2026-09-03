# Discordia

Plataforma de chat con servidores, canales de texto y voz, mensajeria en tiempo real
y moderacion. Grupo 15.

| Repositorio | Responsabilidad | Stack |
|---|---|---|
| `gateway` | Punto unico de entrada: routing, validacion de token, rate limiting | Go |
| `identity-service` | Usuarios, autenticacion, perfil, suspension de cuenta, rol staff | Python |
| `community-service` | Servidores, canales, roles y permisos, moderacion | Python |
| `payment-service` | Premium y cobros | Python |
| `messaging-service` | Mensajes, historial, tiempo real, DMs | Go |
| `voice-service` | Canales de voz, tokens de sesion, presencia | Go |
| `notification-service` | No leidos, preferencias, push | Go |
| `clients` | Monorepo: cliente web y app mobile | TypeScript |
| `backoffice` | Panel de administracion | TypeScript |
| `local-env` | Compose que levanta todo el sistema | Docker |
| `docs` | ADRs, diagramas C4, contratos OpenAPI | Markdown |

Los clientes no hablan con un servicio directamente: todo pasa por el `gateway`.

Backlog: [tablero del proyecto](https://github.com/orgs/Discordia-Grupo-15/projects/1).
Las historias son issues del repo `docs`.
