command=$1
if [ $# -eq 0 ] ; then 
    command=none
fi


if [[ ! -f src/tinyassign/tinyhouse/Pedigree.py ]] ; then
    echo Pedigree.py file not found. Check that the tinyhouse submodule is up to date
    exit 
fi

# Create python wheel.
rm -r build
rm -r dist
python setup.py bdist_wheel

if [ $command == "install" ] ; then
    pip uninstall AlphaAssign -y
    pip install dist/AlphaAssign-0.0.1-py3-none-any.whl
fi

#Compile manual
 ( cd docs; make latexpdf )


target=AlphaAssign
rm -rf $target
mkdir $target

# Moves the wheel over
cp dist/* $target 

# Moves the manual over
cp docs/build/latex/AlphaAssign.pdf $target 

# Move the examples over
cp -r example $target
chmod 770 $target/example/run_examples.sh
zip -r $target.zip AlphaAssign

