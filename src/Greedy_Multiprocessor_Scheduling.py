from BranchBound import branchBoundSolutionWithGreedy as branch_bound_solution
from BnB import branchBoundSolutionBase as branch_bound_solution_base
def main():
    job1 = [10, 9, 8, 7, 6, 5, 4]
    cpu1 = 3
    find_solution(job1, cpu1)
    # branch_bound_solution(find_solution(job1, cpu1))
    # branch_bound_solution_base(job1, cpu1)

def re_sort_dict(cpu_list):
    index = len(cpu_list)
    cpu_list_2 = iter(cpu_list)
    prev_cpu = {}
    prev_key = ""
    for x in cpu_list_2:
        curr_cpu = cpu_list[x]
        if(not prev_cpu):
            prev_cpu = curr_cpu
            prev_key = x
            continue
        if(prev_cpu["time"] > curr_cpu["time"]):
            # swap
            new_first = {"time" : curr_cpu["time"], "list_of_processes" : curr_cpu["list_of_processes"]}
            new_second = {"time" : prev_cpu["time"], "list_of_processes" : prev_cpu["list_of_processes"]}
            cpu_list[prev_key] = new_first
            cpu_list[x] = new_second
        elif(prev_cpu["time"] <= curr_cpu["time"]):
            return
        prev_key = x

def find_solution(job_list, num_of_cpus):
    # sort job list in descending order
    job_list.sort(reverse = True)

    # empty cpu dictionary
    cpu_list = {}
    for i in range(1,num_of_cpus+1):
        n_cpu = "cpu"+str(i)
        entry = {"time" : 0, "list_of_processes": []}
        cpu_list[n_cpu] = entry

    # for each job, add to cpu with smallest total time
    # which will be first, since dict is sorted
    for el in job_list:
        first_cpu = next(iter(cpu_list.values()), None)
        first_cpu["time"] += el
        l = first_cpu["list_of_processes"]
        l.append(el)
        first_cpu.update({"list_of_processes":l})
        # make sure newly updated dict entry at index 0 is in correct spot 
        re_sort_dict(cpu_list)
    print("Optimal Job Configuation", cpu_list)
    last_cpu = "cpu"+str(num_of_cpus)
    print("Total Time:", cpu_list[last_cpu]["time"])

if __name__ == "__main__":
    main()