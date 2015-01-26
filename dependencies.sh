git clone https://github.com/ProjetPP/Scripts.git
cd Scripts
./bootstrap_corenlp.sh
CORENLP="stanford-corenlp-full-2014-08-27" CORENLP_OPTIONS="-parse.flags \" -makeCopulaHead\"" python3 -m corenlp &
