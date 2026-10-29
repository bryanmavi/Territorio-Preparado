"""Copy the operations center into the compiled app without rebuilding its bundles."""
from pathlib import Path
import shutil
frontend=Path(__file__).resolve().parents[1];source=frontend/'operations-source';dist=frontend/'dist'
for name,target in [('disaster-ai.html',dist/'disaster-ai.html'),('disaster-ai.js',dist/'assets/disaster-ai.js'),('operations.html',dist/'operations.html'),('operations.css',dist/'assets/operations.css'),('operations.js',dist/'assets/operations.js'),('operations-entry.js',dist/'assets/operations-entry.js')]:
 shutil.copy2(source/name,target)
index=dist/'index.html';content=index.read_text();script='<script src="./assets/operations-entry.js"></script>'
if 'operations-entry.js' not in content:index.write_text(content.replace('</body>',script+'</body>'))
print('Integrated operations center; existing map and simulation bundles preserved.')

# Reapply the shared visual system after generating app pages.
import runpy
runpy.run_path(str(Path(__file__).resolve().parent / "integrate_design.py"), run_name="__main__")
