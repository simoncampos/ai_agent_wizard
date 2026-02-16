#!/usr/bin/env python3
"""
AI Agent Wizard - Instalador Simple
Indexación inteligente para agentes de IA: elimina navegación, reduce tokens 95%
Wrapper que llama al main.py del src/
"""

import sys
import os

# Agregar src al path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

# Importar y ejecutar main
from main import main

if __name__ == '__main__':
    main()
