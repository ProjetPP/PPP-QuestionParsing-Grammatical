
## Hierarchy_analysis review

? : currend choice is very bad
! : current choice is very good

What was the monetary value of the Nobel Peace Prize in 1989? 
What is the name of the managing director of Apricot Computer?
  ? merge amod
  
What country is the biggest producer of tungsten? 
Who was the first Taiwanese President?
Who was the first American in space?
What is the largest city in Germany?
  ! not merge amod
  
How long did the Charles Manson murder trial last?
What two US biochemists won the Nobel Prize in medicine in 1992?
  ? not merge nn

What was the monetary value of the Nobel Peace Prize in 1989? 
Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?
Where was Ulysses S. Grant born?
  ! merge nn
  
Where is Inoco based?
Where was George Washington born?
  ? nsubjpass
  
What is the brightest star visible from Earth?
  cop not removed!
  change what <-> is

Where does most of the marijuana entering the United States come from?
  ? merge prep (when it's not prep_x) 

What did John Hinckley do to impress Jodie Foster?
  ? collapse dobj to comp
    
* Treat nn as mod (and not merge)

## Question word to triples

Depends on question word is nsubj(pass) or not:
  Who's been killed by Oswald?
  Who is the president by Oswald?
  What has been done after the war?
