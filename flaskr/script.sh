#!/bin/bash

print_help () {
    echo "usage: script.sh advance"
    echo "       script.sh add amount people..."
    echo "       script.sh run"
    echo ""
    echo "       amount - amount of finance to add"
    echo "       people - receiving users"
}

case "$1" in
    "add")
        shift
        amount="$1"
        shift
        while (("$#"))
        do
            python3 powerPlants.py user changeFinance "$1" "$amount"
            echo "$1"
            shift
        done
        ;;
    "advance")
        shift
        amount=($(python3 powerPlants.py plant list | wc -l))
        amount=$(( amount - 1 ))
        i=1
        while [ "$i" -le "$amount" ]
        do
            python3 powerPlants.py plant advance "$i"
            i=$((i + 1))
        done
        ;;
    "run")
        gunicorn --bind 0.0.0.0:5000 wsgi:app
        ;;
    *)
        echo "Uknown arg"
        print_help
        ;;
esac
