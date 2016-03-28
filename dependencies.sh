git clone https://github.com/ProjetPP/Deployment.git
cd Deployment
./bootstrap_corenlp.sh --nouser

export JAVA_PATH=/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
if [ ! -f $JAVA_PATH ]
then
    export JAVA_PATH=/usr/lib/jvm/java-8-oracle/bin/java
fi
cd CoreNLP
export CLASSPATH="`find . -name '*.jar'`"
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer &
sleep 1 # Let the server some time to start...
echo "CoreNLP server launched in background: PID $! "
