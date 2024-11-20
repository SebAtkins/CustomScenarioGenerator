from random import randint, shuffle

def genScenario(maxTasks, maxUsers, maxTeams, maxConstraints):
    scenario = ""

    tasks = randint(2, maxTasks)
    users = randint(2, maxUsers)
    teams = randint(2, maxTeams)
    if teams > users:
        teams = users - 1
    constraints = randint(2, maxConstraints)

    scenario += f"#Tasks: {tasks}\n"
    scenario += f"#Users: {users}\n"
    scenario += f"#Teams: {teams}\n"

    userList = [u for u in range(users)]
    shuffle(userList)
    teamList = []

    for t in range(teams):
        team = []
        teamSize = 1
        if (int)(users / teams) > 1:
            teamSize = randint(1, (int)(users / teams))
        for u in range(teamSize):
            team.append(userList.pop(0))
        teamList.append(team)
    for team in teamList:
        teamString = ""
        for user in team:
            teamString += f"u{user + 1} "
        scenario += teamString + "\n"
    
    scenario += f"#Constraints: {constraints}\n"

    authorised = [u for u in range(users)]
    shuffle(authorised)

    for c in range(constraints):
        constraint = randint(0, 7)
        match constraint:
            case 0:
                authorisedUser = authorised.pop(0)
                authorisedTasks  = [t for t in range(tasks) if randint(0, 4) == 0]
                scenario += f"Authorisations u{authorisedUser + 1} "
                for t in authorisedTasks:
                    scenario += f"t{t + 1} "
                scenario += "\n"
            case 1:
                scenario += f"Separation-of-duty t{randint(1, tasks)} t{randint(1, tasks)}\n"
            case 2:
                scenario += f"Binding-of-duty t{randint(1, tasks)} t{randint(1, tasks)}\n"
            case 3:
                includedTasks  = [t for t in range(tasks) if randint(0, 4) == 0]
                if len(includedTasks) == 0:
                    includedTasks = [0]
                scenario += f"At-most-k {randint(1, tasks)} "
                for t in includedTasks:
                    scenario += f"t{t + 1} "
                scenario += "\n"
            case 4:
                includedTasks  = [t for t in range(tasks) if randint(0, 4) == 0]
                if len(includedTasks) == 0:
                    includedTasks = [0]
                scenario += f"EC1 {randint(1, tasks)} "
                for t in includedTasks:
                    scenario += f"t{t + 1} "
                scenario += "\n"
            case 5:
                includedTeams  = [t for t in range(teams) if randint(0, 4) == 0]
                if len(includedTeams) == 0:
                    includedTeams = [0]
                includedTasks  = [t for t in range(tasks) if randint(0, 4) == 0]
                if len(includedTasks) == 0:
                    includedTasks = [0]
                scenario += "EC2 "
                for t in includedTeams:
                    scenario += f"team{t + 1} "
                for t in includedTasks:
                    scenario += f"t{t + 1} "
                scenario += "\n"
            case 6:
                scenario += f"EC3 team{randint(1, teams)} {randint(1, tasks - 1)}\n"
            case 7:
                scenario += f"EC4 team{randint(1, teams)} u{randint(1, users)}\n"

    return scenario

def makeScenario(userCount, count = 10):
    i = 0
    failedScenarios = 0

    while i < count:
        try:
            text = genScenario(userCount, userCount, (int)(userCount / 2), userCount * 2)
            with open(f"custom/{userCount}/scenario{i}.txt", "w") as file:
                file.write(text)
            i += 1
        except:
            failedScenarios += 1
    
    print(f"Failed scenarios: {failedScenarios}")

userCounts = [10, 20, 50, 100, 200, 300, 400, 500]
for i in userCounts:
    makeScenario(i, 500)