git clone https://github.com/ProjetPP/Scripts.git
cd Scripts
./bootstrap_corenlp.sh --nouser

export JAVA_PATH=/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
if [ ! -f $JAVA_PATH ]
then
    export JAVA_PATH=/usr/lib/jvm/java-8-oracle/bin/java
fi
CORENLP="stanford-corenlp-full-*" CORENLP_OPTIONS="-parse.flags \" -makeCopulaHead\"" python3 -m corenlp &
