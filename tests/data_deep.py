from ppp_datamodel import Triple, Resource, Missing, Intersection, Exists, First, Last, Sort

# expected[q] is the expected tree produced by the module for the question q.

expected = {
    'What is the birth date of Bob Marley?':
    Triple(
        Resource('Bob Marley'),
        Resource('birth date'),
        Missing()
    ),

    'When was born the daughters of the wife of the president of the United States?':
    Triple(
        Triple(
            Triple(
                Triple(
                    Resource('United States'),
                    Resource('president'),
                    Missing()
                ),
                Resource('wife'),
                Missing()
            ),
            Resource('daughter'),
            Missing()
        ),
        Resource('birth date'),
        Missing()
    ),

    'Who wrote "Le Petit Prince" and "Vol de Nuit"':
    Intersection([
        Triple(
            Resource('Le Petit Prince'),
            Resource('writer'),
            Missing()
        ),
        Triple(
            Resource('Vol de Nuit'),
            Resource('writer'),
            Missing()
        )
    ]),

    'Is there a capital of France?':
    Exists(
        Triple(
            Resource('France'),
            Resource('capital'),
            Missing()
        )
    ),

    'What is the highest mountain in the world?':
    Last(
        Sort(
            Triple(
                Resource('world'),
                Resource('mountain'),
                Missing()
            ),
            Resource('height')
        )
    ),

    'Give me the capital of Australia.':
    Triple(
        Resource('Australia'),
        Resource('capital'),
        Missing()
    ),

    'What is the English for "星際大戰四部曲：曙光乍現"?':
    Triple(
        Resource('星際大戰四部曲：曙光乍現'),
        Resource('English'),
        Missing()
    ),

    'What is the English for "حرب النجوم الجزء الخامس: الإمبراطورية تعيد الضربات"?':
    Triple(
        Resource('حرب النجوم الجزء الخامس: الإمبراطورية تعيد الضربات'),
        Resource('English'),
        Missing()
    ),

    'What is the English for "Звёздные войны. Эпизод VI: Возвращение джедая"?':
    Triple(
        Resource('Звёздные войны. Эпизод VI: Возвращение джедая'),
        Resource('English'),
        Missing()
    ),
}
