#### assistant.py
#### Matt Manzi
#### 2018-03-19
#### The user interacts with Assistant to ask for help with simple tasks
#### including addition, multiplication, and exponentiating numbers.
import logging
import json
import re
import constants as c
import skills as sk



def initLog():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger("AssistantLog")
    return log

LOG = initLog()



def loadKnowledge():
    """Safely loads the Assistant's Knowledge

    Opens the JSON file named by c.KNOWLEDGE and loads it into a dict object

    Returns:
        A dict mapping the Assistant's skills to a variety of parameters
        required to use that skill.  For example, a skill may look like:

        "add": {
            "params": 2,
            "paramType": "int",
            "returns": 1,
            "returnType": "int",
            "grammar": ".*(add|combine|sum|addition|all)\\s+(?P<p0>\\d+)\\s+(and|\\+|&|plus)\\s+(?P<p1>\\d+).*",
            "keywords": "(add|combine|sum|addition|all)"
        }
         - corresponding to -
         knowledge["add"]

    Raises:
        OSError: An error occurred reading the Knowledge file from storage
        JSONDecodeError: An error occurred parsing the Knowledge file
    """

    try:
        knowledgeFile = open(c.KNOWLEDGE, "r")
    except:
        LOG.error("Unable to load Knowledge, ensure that \"%s\" is in the current directory.", c.KNOWLEDGE)
        raise
    else:
        LOG.debug("Opened Knowledge from: %s", c.KNOWLEDGE)

    try:
        return json.load(knowledgeFile)
    except:
        LOG.error("Unable to load Knowledge, ensure that the JSON file is properly formatted.")
        raise
    finally:
        knowledgeFile.close()



def findSkills(knowledge, task):
    """Finds matching skills in Knowledge
    """

    skills = []
    for skill in knowledge:

        # if task matches exactly
        if re.fullmatch(knowledge[skill][c.GRAMMAR], task, re.I) != None:
            skills.append((skill, True))
        # if task matches skill keyword(s)
        elif re.match(knowledge[skill][c.KEYWORDS], task, re.I) != None:
            skills.append((skill, False))

    LOG.debug("Matching skills: %s", skills)
    return skills



def executeTask(knowledge, skill, task):
    """Builds and evaluates a skill from the task
    """

    finalSkill = c.SKILLS + "." + skill

    # extract skill information
    skillGrammar = knowledge[skill][c.GRAMMAR]
    numParams = knowledge[skill][c.NUM_PARAM]
    numReturns = knowledge[skill][c.NUM_RET]
    typeReturn = knowledge[skill][c.TYPE_RET]
    LOG.debug("num params/returns: %d/%d", numParams, numReturns)

    # match the full skill
    match = re.fullmatch(skillGrammar, task, re.I)

    # extract parameters for the skill
    params = []
    for i in range(numParams):
        LOG.debug("Extracting parameter %d", i)
        param = match.group("p" + str(i))

        # add quotes for string params
        if knowledge[skill][c.TYPE_PARAM] == c.STRING_T:
            param = "\"" + param + "\""

        params.append(param)

    LOG.debug("Parameters: %s", params)

    finalSkill += "(" + ",".join(params) + ")" # add parameters
    finalSkill = typeReturn + "(" + finalSkill + ")" # return type cast
    LOG.debug("Final skill string is: %s", finalSkill)

    # evaluate the task
    answer = eval(finalSkill)

    # print the result (if relevant)
    if numReturns == 1:
        print("My answer is", answer)
    elif numReturns > 1:
        print("Results:\n")
        for a in answer:
            print("\t", a)



def main():
    LOG.debug("Entered main")

    # load Knowledge
    knowledge = loadKnowledge()
    LOG.debug("Knowledge loaded and availabe in dict")

    # prompt for task (primer)
    task = input("How can I help you today? ").lower()
    LOG.debug("Task: %s", task)

    # accepting tasks
    while re.fullmatch(c.EXIT_TASK, task) == None:

        # find matching skills
        skills = findSkills(knowledge, task)

        # no posiblities
        if len(skills) == 0:
            print("I didn't understand that, try asking for help.")

        # multiple posiblities
        elif len(skills) > 1:
            print("I'm not sure what exactly you'd like to do. Did you want to:")
            for s in skills:
                print("\t", s[c.F_SKILL_NAME].capitalize(), "(Top Match)" if s[1] else "")

        # single, full-matching skill!
        elif skills[0][c.F_SKILL_FULL]:
            executeTask(knowledge, skills[0][c.F_SKILL_NAME], task)

        # nothing truly matches
        else:
            print("I didn't understand the format of your request, try again.")

        # newline space for next prompt
        print()

        # prompt for task
        task = input("How can I help you today? ").lower()
        LOG.debug("Task: %s", task)

    print("Have a nice day!")

main()
