#!/bin/bash
set -x
PACKAGE=syct-0.4.5*
pip install --upgrade build twine
python -m build
python -m twine upload dist/${PACKAGE}
