def branchBoundSolutionWithGreedy(cpu_list):
    #again we use the dictionary because its mutable only difference is we are setting them to the greedy solutions result
    best = {
        "tallest": max(sum(i) for i in cpu_list),
        "assignment": [i[:] for i in cpu_list],
    }
    #look at comment for the computeLowerBound function
    lowerBound = computeLowerBound(cpu_list)
    #use a set to see where we have visited to avoid lookinging at already explored branches. We use a set specifically because its hashable and therefore way faster to check if values are in there
    visited = set() 
    #our recursive function and print statenent
    explore(cpu_list, best, lowerBound, visited)
    print(f"Optimal assignment: {best['assignment']}, tallest: {best['tallest']}")
    return best["assignment"]

def explore(cpus, best, lowerBound, visited):
    #look below but just making data work with sets for pure optimization purposes
    state = canonical(cpus)
    #just check if we need to explore this branch or if its already been visited
    if state in visited:
        return
    visited.add(state)
#just comparing solution at current branch to the greedy solution
    currentTallest = max(sum(i) for i in cpus)

    if currentTallest < best["tallest"]:
        best["tallest"] = currentTallest
        best["assignment"] = [i[:] for i in cpus]
#checking if we found the optimal solution and are finished
    if currentTallest == lowerBound:
        return
#get the cpu with the most work
    tallestIndex = max(range(len(cpus)), key=lambda i: sum(cpus[i]))
#we just try moving every job from the cpu with the most work to every other cpu and then explore the new branches. We then back track that manuver and try the next one
    for jobPosition in range(len(cpus[tallestIndex])):
        job = cpus[tallestIndex][jobPosition]
        for targetIndex in range(len(cpus)):
            if targetIndex == tallestIndex:
                continue
            cpus[tallestIndex].pop(jobPosition)
            cpus[targetIndex].append(job)
            explore(cpus, best, lowerBound, visited)
            cpus[targetIndex].pop()
            cpus[tallestIndex].insert(jobPosition, job)
#instead of just moving jobs here we are swapping every job on the most worked cpu with every job on every other cpu and then again backtrack and try the next swap
    for aPosition in range(len(cpus[tallestIndex])):
        jobA = cpus[tallestIndex][aPosition]
        for targetIndex in range(len(cpus)):
            if targetIndex == tallestIndex:
                continue
            for bPosition in range(len(cpus[targetIndex])):
                jobB = cpus[targetIndex][bPosition]
                if jobA <= jobB:
                    continue
                cpus[tallestIndex][aPosition] = jobB
                cpus[targetIndex][bPosition] = jobA
                explore(cpus, best, lowerBound, visited)
                cpus[tallestIndex][aPosition] = jobA
                cpus[targetIndex][bPosition] = jobB

#we are just turning our list of lists into a tuple of tuples so that we can hash it and make it compatible with sets.
def canonical(cpus):
    return tuple(sorted(tuple(sorted(i)) for i in cpus))

#we are just finding the situation in which all cpus have the exact same amount of work so we could stop immediately if we find it
def computeLowerBound(cpus):
    allJobs = [j for i in cpus for j in i]
    #just total max / number of cpus rounded up and telling the function that the minimum tallest value is the biggest job
    return max(max(allJobs), -(-sum(allJobs) // len(cpus)))


            
