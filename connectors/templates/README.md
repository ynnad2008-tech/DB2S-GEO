# Plantilla de conector

Copiar esta carpeta para crear un nuevo conector:

1. Duplicar `templates/` → `connectors/<fuente>/`
2. Completar `manifest.yaml`
3. Ajustar `connector.py` heredando de `BaseConnector`
4. Documentar en `README.md` de la fuente
5. Registrar en el catálogo documental (`docs/06_...`)

**No** implementar acceso real hasta la fase correspondiente.