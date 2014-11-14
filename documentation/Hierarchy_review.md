
? : currend choice is very bad
! : current choice is very good

appos
=====

Who came up with the name, El Nino?
  ? merge appos

amod
====
  
What was the monetary value of the Nobel Peace Prize in 1989? 
What is the name of the managing director of Apricot Computer?
Who held the endurance record for women pilots in 1929?
Who is the prime minister of Japan?
Who is the Greek God of the Sea?
Who invented the hula hoop?
  ? not merge amod
  
What country is the biggest producer of tungsten? 
Who was the first Taiwanese President?
Who was the first American in space?
What is the largest city in Germany?
Who was the 23rd president of the United States?
Who is the tallest man in the world?
  ! not merge amod

nn
==
  
How long did the Charles Manson murder trial last?
What two US biochemists won the Nobel Prize in medicine in 1992?
  ? not merge nn
  
What was the monetary value of the Nobel Peace Prize in 1989? 
Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?
Where was Ulysses S. Grant born?
  ! merge nn

nsubjpass
=========
  
Where is Inoco based?
Where was George Washington born?
  ? nsubjpass

cop
===
  
What is the brightest star visible from Earth?
  cop not removed!
  change what <-> is

prep
====

Where does most of the marijuana entering the United States come from?
  ? merge prep (when it's not prep_x) 

Level up prep_x in order not to have a -prep-> b -prep-> c
  Who was President of Afghanistan in 1994? (juste pour of -> in)
  Who won two gold medals in skiing in the Olympic Games in Calgary?
or not : 
  Who followed Willy Brandt as chancellor of the Federal Republic of Germany?
  
dobj
====

dobj = t2 or t4?

What did John Hinckley do to impress Jodie Foster?
  ? collapse dobj to comp
  ? dobj is impossible

When did they won the lottery?
  ? dobj = t4
  
Who killed Gandhi?
  ! dobj = t2
   
pobj
====

(map to comp temporarily)

Who is the author of "Twenty Thousand Leagues Under the Sea"?
Who is Bob according to you?
  ? pobj impossible 

dep
===

Who wrote the song, "Stardust"?

vmod
====

Who was the second man to walk on the moon?

nsubj
=====

only if a = is/was/... ?
