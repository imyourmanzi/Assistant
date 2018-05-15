#### Matt Manzi
#### 2018-03-21
#### Constants for Assistant

KNOWLEDGE = "knowledge.json"
SKILLS    = "sk"
EXIT_TASK = ".*(exit|quit|leave|goodbye).*"

## knowledge.json skill fields
DESC        = "description"
NUM_PARAM   = "params"
TYPE_PARAM  = "paramType"
NUM_RET     = "returns"
TYPE_RET    = "returnType"
GRAMMAR     = "grammar"
KEYWORDS    = "keywords"

## knowledge.json skills' types
INT_T    = "int"
FLOAT_T  = "float"
STRING_T = "str"

## findSkills() return fields
F_SKILL_NAME = 0
F_SKILL_FULL = 1
