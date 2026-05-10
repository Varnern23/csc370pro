def branchBoundSolutionBase(jobList, num_cpus):
    #we make sure the jobs are sorted
    jobList = sorted(jobList, reverse=True)
    #use a dictionary to store solution becuase its mutable adn easier to update recursively
    best = {
        "tallest": float('inf'),
        "assignment": None,
    }
    #initialize some empty lists to represent the cpus and use an explicit stack instead of recursion
    cpus = [[] for x in range(num_cpus)]
    explore(jobList, cpus, best)
    print(f"Optimal assignment: {best['assignment']}, tallest: {best['tallest']}")
    return best["assignment"]

#iterative function to explore all possible assignments using an explicit stack to avoid hitting pythons recursion limit
def explore(jobList, cpus_init, best):
    #each entry on the stack is a (jobIndex, cpus_snapshot) pair representing a branch to explore
    stack = [(0, [list(i) for i in cpus_init])]
    while stack:
        jobIndex, cpus = stack.pop()
        #base case we just check if all jobs have been assigned and make comparisons to our best solution at the time
        if jobIndex == len(jobList):
            tallest = max(sum(i) for i in cpus)
            if tallest < best["tallest"]:
                best["tallest"] = tallest
                best["assignment"] = [list(i) for i in cpus]
            continue
        #we prune branches here that we already know will not lead to a better solution
        current_tallest = max(sum(i) for i in cpus)
        if current_tallest >= best["tallest"]:
            continue
        #we now push all possible assignments for the current job onto the stack to explore later
        job = jobList[jobIndex]
        for i in range(len(cpus)):
            new_cpus = [list(c) for c in cpus]
            new_cpus[i].append(job)
            stack.append((jobIndex + 1, new_cpus))
