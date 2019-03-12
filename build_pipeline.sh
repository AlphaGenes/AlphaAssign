rm -r build
rm -r dist
python setup.py bdist_wheel
pip uninstall AlphaAssign -y
pip install dist/AlphaAssign-0.0.1-py3-none-any.whl
