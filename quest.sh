#!/bin/bash
ORIG_DIR=$PWD
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURRENT_VENV=$VIRTUAL_ENV

cd $SCRIPT_DIR

if [ ! -e "$SCRIPT_DIR/venv" ] ; then
    echo "initializing virtualenv in $SCRIPT_DIR/venv"
    python bootstrap.py
else
    echo "$SCRIPT_DIR/venv exists"
    echo "skipping virtualenv initialization"
fi

if [ "$CURRENT_VENV" != "$SCRIPT_DIR/venv" ] ; then
    source venv/bin/activate
fi

python quest.py init provision

if [ "$CURRENT_VENV" != "$SCRIPT_DIR/venv" ] ; then
    echo "entering a nested bash"
    echo "please type \`exit\` to return to your normally scheduled shell"
    /bin/bash --rcfile venv/bin/activate
fi

cd $ORIG_DIR

