#!/bin/bash
COMMAND="FALSE"
DOC="FALSE"
INSTALL="FALSE"
DOCS="FALSE"
TEST="FALSE"
RSYNC="FALSE"
POSITIONAL=()
if [[ $# -eq 0 ]] ; then
    echo 'Usage: -options'
    echo -e 'Options:\n -i -> executable generation,\n -d -> documentation generation,\n -t -> unit testing,\n -e -> execute python script,\n -dox -> Doxygen documentation (deprecated),\n -s -> rsync with server to update files'
    exit 0
fi
while [[ $# -gt 0 ]]
do
    key="$1"
    
    case $key in
        -e|--execute)
            COMMAND="TRUE"
            shift # past argument
        ;;
        -dox|--doxygen)
            DOC="TRUE"
            shift
        ;;
        -i|--install)
            INSTALL="TRUE"
            shift
        ;;
        -d|-documentation)
            DOCS="TRUE"
            shift
        ;;
        -t|-test)
            TEST="TRUE"
            shift
        ;;
        -s|--sync)
            RSYNC="TRUE"
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
    cp dynamic_commands/executable/dist/smartOBD dynamic_commands/smartOBDexecutable
fi


if [ $COMMAND = "TRUE" ]
then
    sudo python dynamic_commands/main.py
fi

if [ $DOCS = "TRUE" ]
then
    cd dynamic_commands/docs
    make html
    make latexpdf
    cd ..
    cd ..
    cp dynamic_commands/docs/build/latex/smartobd.pdf dynamic_commands/documentation.pdf
fi

if [ $TEST = "TRUE" ]
then   
    cd dynamic_commands/tests
    pytest test.py
    cd ..
    cd ..
fi

if [ $RSYNC = "TRUE" ]
then
    rsync -avP --exclude '.*' codehawk@198.23.146.166:/home/codehawk/ SmartOBD/
fi