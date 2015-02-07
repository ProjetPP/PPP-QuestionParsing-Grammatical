from ppp_datamodel import Triple as T
from ppp_datamodel import Resource as R
from ppp_datamodel import Missing as M
from ppp_datamodel import Intersection as I
from ppp_datamodel import Union as U
from ppp_datamodel import Exists as E
from ppp_datamodel import First as F
from ppp_datamodel import Last as L
from ppp_datamodel import Sort as S

# expected[q] is the expected tree produced by the module for the question q.

expected = {
    'Who is the prime minister of France?':
    T(R('France'), R('prime minister'), M()),

    'Who is Homer J. Simpson?':
    T(R('Homer J. Simpson'), R('identity'), M()),

    'Who is the France\'s prime minister?':
    T(R('France'), R('prime minister'), M()),

    'What is the birth date of Bob Marley?':
    T(R('Bob Marley'), R('birth date'), M()),

    'When was born the daughters of the wife of the president of the United States?':
    T(
        T(
            T(
                T(R('United States'), R('president'), M()),
                R('wife'),
                M()
            ),
            R('daughter'),
            M()
        ),
        R('birth date'),
        M()
    ),

    'Who wrote "Le Petit Prince" and "Vol de Nuit"':
    I([
        T(R('Le Petit Prince'), R('writer'), M()),
        T(R('Vol de Nuit'), R('writer'), M())
    ]),

    'Is there a capital of France?':
    E(T(R('France'), R('capital'), M())),

    'Is there a pilot in the plane?':
    E(T(R('plane'), R('pilot'), M())),

    'What is the highest mountain in the world?':
    L(
        S(
            T(R('world'), R('mountain'), M()),
            R('height')
        )
    ),

    'Give me the capital of Australia.':
    T(R('Australia'), R('capital'), M()),

    'List books by Roald Dahl.':
    T(R('Roald Dahl'), R('book'), M()),

    'What is the English for "星際大戰四部曲：曙光乍現"?':
    T(R('星際大戰四部曲：曙光乍現'), R('English'), M()),

    'What is the English for "حرب النجوم الجزء الخامس: الإمبراطورية تعيد الضربات"?':
    T(R('حرب النجوم الجزء الخامس: الإمبراطورية تعيد الضربات'), R('English'), M()),

    'What is the English for "Звёздные войны. Эпизод VI: Возвращение джедая"?':
    T(R('Звёздные войны. Эпизод VI: Возвращение джедая'), R('English'), M()),

    'List movies directed by Spielberg.':
    I([
        T(M(), R('instance of'), R('movie')),
        T(M(), R('director'), R('Spielberg'))
    ]),

    'Which books were authored by Victor Hugo?':
    I([
        T(M(), R('instance of'), R('book')),
        T(M(), R('author'), R('Victor Hugo'))
    ]),

    'Which president has been killed by Oswald?':
    I([
        T(M(), R('instance of'), R('president')),
        T(M(), R('killer'), R('Oswald'))
    ]),
    
    'Who invented the hula hoop?':
    T(R('hula hoop'),R('inventor'),M()),

    'Who was killed by Oswald?':
    T(M(), R('killer'), R('Oswald')),

    'Which books did Suzanne Collins write?':
    I([
        T(M(), R('instance of'), R('book')),
        T(M(), R('author'), R('Suzanne Collins'))
    ]),

    'president of France?':
    T(R('France'),R('president'),M()),

    'Give us the queen of England':
    T(R('England'),R('queen'),M()),

    'Who is Babar?':
    T(R('Babar'),R('identity'),M()),

    'What did George Orwell write?':
    T(M(),R('author'),R('George Orwell')),

    'Who has written \"The Hitchhiker\'s Guide to the Galaxy\"?':
    T(R('The Hitchhiker\'s Guide to the Galaxy'),R('author'),M()),

    'When was the president of the United States born':
    T(
        T(R('United States'),R('president'),M()),
        R('birth date'),
        M()
    ),
    
    'From which country is Alan Turing?':
    I([
        T(M(), R('instance of'), R('country')),
        T(R('Alan Turing'), R('country of citizenship'), M())
    ]),
    
    'In which countries is the Lake Victoria?':
    I([
        T(M(), R('instance of'), R('country')),
        T(R('Lake Victoria'), R('country'), M())
    ]),

    'What actor married John F. Kennedy\'s sister?':
    I([
        T(M(), R('instance of'), R('actor')),
        T(
            T(R('John F. Kennedy'),R('sister'),M()),
            R('husband'),
            M()
        )
    ]),

    'Where was Ulysses S. Grant born?':
    T(R('Ulysses S. Grant'), R('birth place'), M()),

    'Who is the US president?':
    T(R('US'),R('president'),M()),

    'Who is the United States president?':
    T(R('United States'),R('president'),M()),

}
