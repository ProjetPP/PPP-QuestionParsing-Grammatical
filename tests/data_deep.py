from ppp_datamodel import Triple as T
from ppp_datamodel import Resource as R
from ppp_datamodel import Missing as M
from ppp_datamodel import Intersection as I
from ppp_datamodel import Union as U
from ppp_datamodel import Exists as E
from ppp_datamodel import First as F
from ppp_datamodel import Last as L
from ppp_datamodel import Sort as S
from ppp_datamodel import List as Li

# expected[q] is the expected tree produced by the module for the question q.
# Warning: be careful before changing a question (e.g. the parsing depends on the uppercase letters)

expected = {
    'Who is the prime minister of France?':
    T(R('France'), R('prime minister'), M()),

    'Who is Homer J. Simpson?':
    T(R('Homer J. Simpson'), R('identity'), M()),

    'Who is the president of France':
    T(R('France'), R('president'), M()),

    'Who is the President of Ghana':
    T(R('Ghana'), R('President'), M()),

    'Who is the France\'s prime minister?':
    T(R('France'), R('prime minister'), M()),

    'What is the birth date of Bob Marley?':
    T(R('Bob Marley'), R('birth date'), M()),

    'How fast is a cheetah?':
    T(R('cheetah'), R('speed'), M()),

    'How wide is a tennis court?':
    T(R('tennis court'), R('width'), M()),

    'How old is Big Ben?':
    T(R('Big Ben'), R('age'), M()),

    'How tall is Burj Khalifa?':
    T(R('Burj Khalifa'), R('height'), M()),

    'How old is the son of the main actor of "I, Robot"?':
    T(
        T(
            T(R('I, Robot'), R('main actor'), M()),
            R('son'),
            M()
        ),
        R('age'),
        M()
    ),

    'How fast is the most expensive car in the World?':
    T(
        L(
            S(
                T(R('World'), R('car'), M()),
                R('cost')
            ),
        ),
        R('speed'),
        M()
    ),

    'When were the daughters of the wife of the president of the United States born?':
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

    'Who are the daughters of the wife of the husband of the wife of the president of the United States?':
    T(
        T(
            T(
                T(
                    T(R('United States'), R('president'), M()),
                    R('wife'),
                    M()
                ),
                R('husband'),
                M()
            ),
            R('wife'),
            M()
        ),
        R('daughter'),
        M()
    ),

    'Who wrote \"Le Petit Prince\" and \"Vol de Nuit\"':
    I([
        T(M(), R('bibliography'), R('Le Petit Prince'), R('author')),
        T(M(), R('bibliography'), R('Vol de Nuit'), R('author'))
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
        T(M(), Li([R('director'), R('directed by')]), R('Spielberg'))
    ]),

    'Who is the director of \"A Clockwork Orange\"?':
    T(R('A Clockwork Orange'),R('director'),M()),

    'Which books were authored by Victor Hugo?':
    I([
        T(M(), R('instance of'), R('book')),
        T(M(), Li([R('authored by'), R('author')]), R('Victor Hugo'), R('bibliography'))
    ]),

    'Which president has been killed by Oswald?':
    I([
        T(M(), R('instance of'), R('president')),
        T(M(), Li([R('killed by'), R('killer')]), R('Oswald'))
    ]),

    'Who invented the hula hoop?':
    T(M(), R('invention'), R('hula hoop'), R('inventor')),

    'Who was killed by Oswald?':
    T(M(), Li([R('killed by'), R('killer')]), R('Oswald')),

    'Which books did Suzanne Collins write?':
    I([
        T(M(), R('instance of'), R('book')),
        T(R('Suzanne Collins'), R('bibliography'), M(), R('author'))
    ]),

    'president of France?':
    T(R('France'), R('president'), M()),

    'Give us the queen of England':
    T(R('England'), R('queen'), M()),

    'Who is Babar?':
    T(R('Babar'), R('identity'), M()),

    'What did George Orwell write?':
    T(R('George Orwell'), R('bibliography'), M(), R('author')),

    'Who has written \"The Hitchhiker\'s Guide to the Galaxy\"?':
    T(M(), R('bibliography'), R('The Hitchhiker\'s Guide to the Galaxy'), R('author')),

    'When was the president of the United States born':
    T(
        T(R('United States'), R('president'), M()),
        R('birth date'),
        M()
    ),

    'What is the birth date of the president of the United States?':
    T(
        T(R('United States'), R('president'), M()),
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
            M(),
            R('wife'),
            T(R('John F. Kennedy'), R('sister'), M()),
            R('married to')
        )
    ]),

    'Who is J. F. Kennedy?':
    T(R('J. F. Kennedy'), R('identity'), M()),

    'Who is J. F. K.?':
    T(R('J. F. K.'), R('identity'), M()),

    'Where was Ulysses S. Grant born?':
    T(R('Ulysses S. Grant'), R('birth place'), M()),

    'What is a chocolate sunday?':
    T(R('chocolate sunday'), R('definition'), M()),

    'What is the D Day?':
    T(R('D Day'), R('definition'), M()),

    'When was D-Day?':
    T(R('D-Day'), R('date'), M()),

    'What is the natural language processing?':
    T(R('natural language processing'), R('definition'), M()),

    'Where is Inoco based?':
    T(R('Inoco'), R('location'), M()),

    'Who is the author of \"Le Petit Prince\"?':
    T(R('Le Petit Prince'), R('author'), M(), R('bibliography')),

    'Who are the Beatles\' members?':
    T(R('Beatles'), R('member'), M()),

    'What is the biggest country in South America?':
    L(
        S(
            T(R('South America'), R('country'), M()),
            R('size')
        )
    ),

    'Who is the author of \"Animal Farm\" and \"1984\"?':
    I([
        T(R('1984'), R('author'), M(), R('bibliography')),
        T(R('Animal Farm'), R('author'), M(), R('bibliography'))
    ]),

    'Who was Darth Vader’s son?':
    T(R('Darth Vader'), R('son'), M()),

    'What was the monetary value of the Nobel Peace Prize in 1989?':
    T(
        T(R('1989'), R('Nobel Peace Prize'), M()),
        R('monetary value'),
        M()
    ),

    'What is the continent of Fiji and Guam?':
    I([
        T(R('Fiji'), R('continent'), M()),
        T(R('Guam'), R('continent'), M())
    ]),

    'Who is the first president of France?':
    F(
        S(
            T(R('France'), R('president'), M()),
            R('default')
        )
    ),

    'What is the most expensive car in the world?':
    L(
        S(
            T(R('world'), R('car'), M()),
            R('cost')
        )
    ),

    'Give the capital of France':
    T(R('France'), R('capital'), M()),

    'Is there a king of England?':
    E(
        T(R('England'), R('king'), M())
    ),

    'What is the highest mountain of Tanzania?':
    L(
        S(
            T(R('Tanzania'), R('mountain'), M()),
            R('height')
        )
    ),

    'What is the coldest place on earth?':
    F(
        S(
            T(R('earth'), R('place'), M()),
            R('temperature')
        )
    ),

    'Who developed Microsoft?':
    T(M(), R('developed'), R('Microsoft'), R('developer')),

    'Give me all companies in Munich':
    T(R('Munich'), R('company'), M()),

    'Where does the prime minister of United Kingdom live?':
    T(
        T(R('United Kingdom'), R('prime minister'), M()),
        R('residence'),
        M()
    ),

    'Where is ENS Lyon?':
    T(R('ENS Lyon'), R('location'), M()),

    'Who was Liz Taylor married to?':
    T(R('Liz Taylor'), R('married to'), M(), R('wife')),

    'What language is spoken in Argentina?':
    I([
        T(M(), R('instance of'), R('language')),
        T(M(), R('spoken in'), R('Argentina'), R('language'))
    ]),

    'What is the capital of India?':
    T(R('India'), R('capital'), M()),

    'What kings ruled on France?':
    I([
        T(M(), R('instance of'), R('king')),
        T(M(), R('ruled on'), R('France'), R('ruler'))
    ]),

    'Who was born on 1984?':
    T(M(), Li([R('born on'), R('birthdate')]), R('1984'), R('birth')),

    'What author is the author of 1984?':
    I([
        T(M(), R('instance of'), R('author')),
        T(R('1984'), R('author'), M(), R('bibliography'))
    ]),

    'Where does David Cameron live':
    T(R('David Cameron'), R('residence'), M()),

    'Where does the animal live?':
    T(R('animal'), R('residence'), M()),

    'Who lives in the farm?':
    T(M(), Li([R('lived in'), R('residence')]), R('farm'), R('inhabitant')),

    'Who wrote \"James and the Giant Peach\"?':
    T(M(), R('bibliography'), R('James and the Giant Peach'), R('author')),

    'What did Roald Dahl write':
    T(R('Roald Dahl'), R('bibliography'), M(), R('author')),

    'What\'s the name of King Arthur\'s sword?':
    T(
        T(R('King Arthur'), R('sword'), M()),
        R('name'),
        M()
    ),

    'What\'s the warmest place on earth?':
    L(
        S(
            T(R('earth'), R('place'), M()),
            R('temperature')
        )
    ),

    'Who\'re the presidents of Europe?':
    T(R('Europe'), R('president'), M()),

    'Where do rocks come from?':
    T(
        R('rock'),
        Li([R('come from'), R('origin')]),
        M()
    ),

    'When was the U.S. capitol built?':
    T(R('U.S. capitol'), R('construction date'), M()),

    'What company manufactures Sinemet?':
    I([
        T(M(), R('instance of'), R('company')),
        T(M(), R('manufactured'), R('Sinemet'))
    ]),

    'How big is the sun?':
    T(R('sun'), R('size'), M()),

    'How long is the Great Barrier Reef?':
    T(R('Great barrier reef'), R('length'), M()),

    'What does S.O.S. stand for?':
    T(R('S.O.S.'), Li([R('meaning'), R('stood for')]), M()),

    'What does \` PSI\' stand for?':
    T(R('PSI'), R('meaning'), M()),

    'What does G.M.T. stand for?':
    T(R('G.M.T.'), R('meaning'), M()),

    'What\'s the tallest piece on a chessboard?':
    L(
        S(
            T(R('chessboard'), R('piece'), M()),
            R('height')
        )
    ),

    'What is the highest peak in Africa?':
    L(
        S(
            T(R('Africa'), R('peak'), M()),
            R('height')
        )
    ),

    'What is artificial intelligence?':
    T(R('artificial intelligence'), R('definition'), M()),

    'What is George Lucas\'s e-mail address?':
    T(R('George Lucas'), R('e-mail address'), M()),

    'What is the definition of cosmology?':
    T(R('cosmology'), R('definition'), M()),

    'What is the name of Miss India 1994?':
    T(R('Miss India 1994'), R('name'), M()),

    'What is the population in India?':
    T(R('India'), R('population'), M()),

    'What is the world\'s population':
    T(R('world'), R('population'), M()),

    'What is the atomic number of polonium?':
    T(R('polonium'), R('atomic number'), M()),

    'What\'s the official language of Algeria?':
    T(R('Algeria'), R('official language'), M()),

    'What are the official languages of the European Union?':
    T(R('European Union'), R('official language'), M()),

    'What\'s the Red Planet?':
    T(R('Red Planet'), R('definition'), M()),

    'What state was Herbert Hoover born in?':
    I([
        T(M(), R('instance of'), R('state')),
        T(R('Herbert Hoover'), Li([R('born in'), R('birthplace')]), M())
    ]),

    'Who was Jean Nicolet?':
    T(R('Jean Nicolet'), R('identity'), M()),

    'What holidays are celebrated in Ireland?':
    I([
        T(M(), R('instance of'), R('holiday')),
        T(M(), R('celebrated in'), R('Ireland'), R('holiday'))
    ]),

    'What state is John F. Kennedy buried in?':
    I([
        T(M(), R('instance of'), R('state')),
        T(R('John F. Kennedy'), Li([R('buried in'), R('location of burial')]), M())
    ]),

    'What chemicals are used in lethal injection?':
    I([
        T(M(), R('instance of'), R('chemical')),
        T(M(), R('used in'), R('lethal injection'))
    ]),

    'What country do the Galapagos Islands belong to?':
    I([
        T(M(), R('instance of'), R('country')),
        T(R('Galapagos Islands'), R('part of'), M())
    ]),

    'What are Brazil\'s national colors?':
    T(R('Brazil'), R('national color'), M()),

    'Which country colonized Hong Kong?':
    I([
        T(M(), R('instance of'), R('country')),
        T(M(), R('colonized'), R('Hong Kong'))
    ]),

    'Where is the Panama Canal?':
    T(R('Panama Canal'), R('location'), M()),

    'Where is the Panama canal?':
    T(R('Panama canal'), R('location'), M()),

    'Who is the daughter of Louis XIV?':
    T(R('Louis XIV'), R('daughter'), M()),

    'Who is Louis XIV?':
    T(R('Louis XIV'), R('identity'), M()),

    'What organization was founded by the Rev. Jerry Falwell?':
    I([
        T(M(), R('instance of'), R('organization')),
        T(M(), Li([R('founded by'), R('foundator')]), R('Rev. Jerry Falwell'))
    ]),

    'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?':
    I([
        T(M(), R('bibliography'), R('Lucy in the Sky with Diamonds'), R('author')),
        T(M(), R('bibliography'), R('Let It Be'), R('author'))
    ]),

    'Where is the deepest trench in atlantic ocean?':
    T(
        L(
            S(
                T(R('atlantic ocean'),R('trench'),M()),
                R('depth')
            )
        ),
        R('location'),
        M()
    ),

    'List the fastest animals in the world':
    L(
        S(
            T(R('world'),R('animal'),M()),
            R('speed')
        )
    ),

    'What is the coldest Planet of the Solar System?':
    F(
        S(
            T(R('Solar System'),R('planet'),M()),
            R('temperature')
        )
    ),

    'Give me the oldest human on earth':
    L(
        S(
            T(R('earth'),R('human'),M()),
            R('age')
        )
    ),

    'Where is the residence of prime minister of india?':
    T(
        T(
            T(R('india'), R('prime minister'), M()),
            R('residence'),
            M()
        ),
        R('location'),
        M()
    ),

    'What is “P=NP”?':
    T(R('P=NP'), R('definition'), M()),

    'What is Head Start?':
    T(R('Head Start'), R('definition'), M()),

    'What is the nationality of Jackson Pollock?':
    T(R('Jackson Pollock'), R('nationality'), M()),

    'What is the zip code for Lyon?':
    T(R('Lyon'), R('zip code'), M()),

    'What is the Boston Strangler\'s name?':
    T(R('Boston Strangler'), R('name'), M()),

    'What is an annotated bibliography?':
    T(R('annotated bibliography'), R('definition'), M()),

    'What is the location of the Great Barrier Reef?':
    T(R('Great Barrier reef'), R('location'), M()),

    'What is the time zone of San Francisco?':
    T(R('San Francisco'), R('time zone'), M()),

    'What is the music genre of Bob Marley?':
    T(R('Bob Marley'), R('music genre'), M()),

	'What is the film genre of Full Metal Jacket?':
    T(R('Full metal jacket'), R('film genre'), M()),
}
