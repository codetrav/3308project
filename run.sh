#!/bin/bash
COMMAND="FALSE"
DOC="FALSE"
INSTALL="FALSE"
POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"
    
    case $key in
        -e|--execute)
            COMMAND="TRUE"
            shift # past argument
        ;;
        -d|--documentation)
            DOC="TRUE"
            shift
        ;;
        -i|--install)
            INSTALL="TRUE"
            shift
        ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


if [ $DOC = "TRUE" ] 
then
    cd dynamic_commands
    doxygen doxygen/Doxyfile
    cd doxygen/latex
    make
    cd ..
    cd ..
    cd ..
    touch dynamic_commands/documentation.pdf
    cp dynamic_commands/doxygen/latex/refman.pdf dynamic_commands/documentation.pdf
fi

if [ $INSTALL = "TRUE" ]
then
    cd dynamic_commands
    pyinstaller --distpath ./executable/dist/ --workpath ./executable/build/ -F --specpath ./executable/ -n smartOBD main.py 
    cd ..
fi


if [ $COMMAND = "TRUE" ]
then
    sudo python dynamic_commands/main.py
fi