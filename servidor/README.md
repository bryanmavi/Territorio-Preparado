# Servidor local del demostrador

Ejecutar desde la raíz del repositorio:

```bash
python3 servidor/server.py --port 4180
python3 -m unittest discover -s servidor -v
```

Abrir http://127.0.0.1:4180/ y entrar a **07 Centro de operaciones**. Solo procesa el conjunto sintético incorporado. SQLite conserva únicamente resultados agregados en `/tmp/territorio-preparado-demo.sqlite` (se puede cambiar con `--db`). El servidor se enlaza a loopback; no es un servicio productivo ni un receptor de censos reales.

- `GET /api/status`: estado del proceso y alcance de la demo.
- `POST /api/demo/reconcile`: consolida 128 reportes en 104 personas únicas y 32 hogares, y registra el resultado local.
- `POST /api/demo/analysis`: analiza agregados sintéticos con un modelo Ollama local previamente instalado. Definir `TP_LOCAL_MODEL` con su nombre; el endpoint del motor está fijado en `127.0.0.1:11434`. Sin modelo configurado, responde 503 y no inventa un análisis.

Las peticiones de navegador son del mismo origen. No se envían datos a servicios comerciales de IA. Autenticación, permisos, cifrado, resiliencia y conectores oficiales de vigilancia son requisitos de la etapa de producción, descritos en `docs/SERVIDOR_PROPIO_IA_Y_VIGILANCIA.md`.
