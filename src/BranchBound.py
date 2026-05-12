def branchBoundSolutionWithGreedy(cpu_list, time):
    #again we use the dictionary because its mutable only difference is we are setting them to the greedy solutions result
    best = {
        "tallest": time,
        "assignment": [list(c) for c in cpu_list],
    }
    #look at comment for the computeLowerBound function
    lowerBound = computeLowerBound(cpu_list)
    #use a set to see where we have visited to avoid lookinging at already explored branches. We use a set specifically because its hashable and therefore way faster to check if values are in there
    visited = set()
    #our explore function and print statement
    explore(cpu_list, best, lowerBound, visited)
    print(f"Optimal assignment: {best['assignment']}, tallest: {best['tallest']}")
    return best["assignment"]


# CHANGED: added max_nodes budget so large inputs don't run forever.
# once we hit the limit we stop exploring and return the best solution found so far
def explore(cpu_list, best, lowerBound, visited, max_nodes=500_000):
    #we use an explicit stack instead of recursion so we dont hit pythons recursion limit on large job lists
    stack = [[list(c) for c in cpu_list]]
    nodes_visited = 0  # CHANGED: track how many states we've explored

    # CHANGED: added nodes_visited < max_nodes as a second exit condition
    while stack and nodes_visited < max_nodes:
        cpus = stack.pop()
        #look below but just making data work with sets for pure optimization purposes
        state = canonical(cpus)
        #just check if we need to explore this branch or if its already been visited
        if state in visited:
            continue
        visited.add(state)
        nodes_visited += 1  # CHANGED: increment node counter each time we explore a new state

        #just comparing solution at current branch to the greedy solution
        currentTallest = max(sum(c) for c in cpus)
        if currentTallest < best["tallest"]:
            best["tallest"] = currentTallest
            best["assignment"] = [list(c) for c in cpus]

        #checking if we found the optimal solution and are finished
        if currentTallest == lowerBound:
            continue

        # CHANGED: prune branches strictly worse than current best.
        # must be > not >= because equal states can still lead to better children
        if currentTallest > best["tallest"]:
            continue

        #get the cpu with the most work
        tallestIndex = max(range(len(cpus)), key=lambda i: sum(cpus[i]))

        #we just try moving every job from the cpu with the most work to every other cpu and push the new state onto the stack to explore later
        for jobPosition in range(len(cpus[tallestIndex])):
            job = cpus[tallestIndex][jobPosition]
            for targetIndex in range(len(cpus)):
                if targetIndex == tallestIndex:
                    continue
                new_cpus = [list(c) for c in cpus]
                new_cpus[tallestIndex].pop(jobPosition)
                new_cpus[targetIndex].append(job)
                # CHANGED: only push if this move doesn't make things strictly worse.
                # use <= instead of < so we still explore moves that stay equal,
                # since those can lead to improvements further down the tree
                new_tallest = max(sum(c) for c in new_cpus)
                if new_tallest <= best["tallest"]:
                    stack.append(new_cpus)

        #instead of just moving jobs here we are swapping every job on the most worked cpu with every job on every other cpu and pushing those states onto the stack
        for aPosition in range(len(cpus[tallestIndex])):
            jobA = cpus[tallestIndex][aPosition]
            for targetIndex in range(len(cpus)):
                if targetIndex == tallestIndex:
                    continue
                for bPosition in range(len(cpus[targetIndex])):
                    jobB = cpus[targetIndex][bPosition]
                    if jobA <= jobB:
                        continue
                    new_cpus = [list(c) for c in cpus]
                    new_cpus[tallestIndex][aPosition] = jobB
                    new_cpus[targetIndex][bPosition] = jobA
                    # CHANGED: same as move pruning — use <= so equal states
                    # still get explored since they can lead to better children
                    new_tallest = max(sum(c) for c in new_cpus)
                    if new_tallest <= best["tallest"]:
                        stack.append(new_cpus)

#we are just turning our list of lists into a tuple of tuples so that we can hash it and make it compatible with sets.
def canonical(cpus):
    return tuple(sorted(tuple(sorted(c)) for c in cpus))

#we are just finding the situation in which all cpus have the exact same amount of work so we could stop immediately if we find it
def computeLowerBound(cpus):
    allJobs = [j for c in cpus for j in c]
    #just total max / number of cpus rounded up and telling the function that the minimum tallest value is the biggest job
    return max(max(allJobs), -(-sum(allJobs) // len(cpus)))