from ppp_datamodel import Triple, Resource, Missing, Intersection, Exists

# expected[q] is the expected tree produced by the module for the question q.

expected = {
    'What is the birth date of George Washington?':
    Triple(
        Resource('George Washington'),
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
}
