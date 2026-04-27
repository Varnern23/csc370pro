def branchBoundSolutionBase(jobList, num_cpus):
    #we make sure the jobs are sorted
    jobList = sorted(jobList, reverse=True)  
    #use a dictionary to store solution becuase its mutable adn easier to update recursively
    best = {
        "tallest": float('inf'),
        "assignment": None,
    }
    #initialize some empty lists to represent the cpus and use calls on methods to explore possible solutions recursively
    cpus = [[] for x in range(num_cpus)]
    explore(jobList, 0, cpus, best)
    print(f"Optimal assignment: {best['assignment']}, tallest: {best['tallest']}")
    return best["assignment"]

#recursive function to explore all possible assignments
def explore(jobList, jobIndex, cpus, best):
    #base case we just check if all jobs have been assigned and make comparisons to our best solution at the time
    if jobIndex == len(jobList):
        tallest = max(sum(i) for i in cpus)
        if tallest < best["tallest"]:
            best["tallest"] = tallest
            best["assignment"] = [i[:] for i in cpus]
        return
    #we prune branches here that we already know will not lead to a better solution
    current_tallest = max(sum(i) for i in cpus)
    if current_tallest >= best["tallest"]:
        return
    #we now explore all possible assignments for the current job
    job = jobList[jobIndex]
    for i in range(len(cpus)):
        cpus[i].append(job)
        explore(jobList, jobIndex + 1, cpus, best)
        cpus[i].pop()