# Proddyt Switch — ferramentas

Moldes e scripts compartilhados pelos 12 forks `Proddyt-Labs/<app>-labs`.

| Arquivo | Pra quê |
|---|---|
| `workflows/labs-release.yml` | Copiado em `.github/workflows/` de cada fork. Push na main (e diário) gera Release com portátil Win/Linux/macOS + instalador Windows. |
| `workflows/sync-upstream.yml` | Copiado em cada fork. Puxa a main do projeto original (storytold) todo dia. |
| `tools/atualizar-portables.ps1` | Baixa o portátil Windows mais novo de cada app pra pasta tester (`C:\DEV\PRODDYT\switch\_portables\`). |

Mudou um molde aqui? Copiar pros 12 forks e commitar em cada um (mesma mensagem).
