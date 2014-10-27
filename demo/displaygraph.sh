if [ $# -lt 1 ] ; then
    echo "Please provide a question."
    exit 1
fi
echo $* | python3 demo4.py | dot -Tps > tmp.ps
evince tmp.ps 2> /dev/null
