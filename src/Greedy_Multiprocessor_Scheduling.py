from BranchBound import branchBoundSolutionWithGreedy as branch_bound_solution
from BnB import branchBoundSolutionBase as branch_bound_solution_base
def main():
    job1 = [10, 9, 8, 7, 6, 5, 4]
    cpu1 = 3
    branch_bound_solution(find_solution(job1, cpu1))
    branch_bound_solution_base(job1, cpu1)
    

def find_smallest(cpu_list, el):
    curr_smallest = sum(cpu_list[0])
    index = 0
    for i in range(len(cpu_list)):
        if(cpu_list[i] == []):
            cpu_list[i] = [el]
            return index
        elif sum(cpu_list[i]) < curr_smallest:
            curr_smallest = sum(cpu_list[i])
            index = i
    cpu_list[index].append(el)
    return index

def find_time(cpu_list):
    largest = sum(cpu_list[0])
    for i in range (1,len(cpu_list)):
        if sum(cpu_list[i]) > largest:
            largest = sum(cpu_list[i])
    return largest

def find_solution(job_list, num_of_cpus):
    # sort job list in descending order
    job_list.sort(reverse = True)
    # empty cpu list
    cpu_list = [[]]*num_of_cpus
    
    # for each job, add to cpu with smallest total time
    for el in job_list:
        index_of_smallest = find_smallest(cpu_list, el)
    print("Optimal Job Configuation", cpu_list)
    total_time = find_time(cpu_list)
    s = (sum([i for i in cpu_list], []))
    s.sort
    print(s)
    print("Total Time:", total_time)
    return cpu_list



if __name__ == "__main__":
    main()