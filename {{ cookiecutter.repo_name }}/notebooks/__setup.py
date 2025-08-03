# notebooks/setup.py

import sys
from pathlib import Path

# Resolve the project root directory
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
