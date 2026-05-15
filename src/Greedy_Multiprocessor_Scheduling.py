import heapq
from BranchBound import branchBoundSolutionWithGreedy as branch_bound_solution
from BnB import branchBoundSolutionBase as branch_bound_solution_base

def main():
    import random
    random.seed(42)
    job1 = [10, 9, 8, 7, 6, 5, 4]
    cpu1 = 3
    optimal, time = find_solution(job1, cpu1)
    branch_bound_solution(optimal, time)

def find_solution(job_list, num_of_cpus):
    # biggest jobs first so we deal with the hard ones early
    job_list.sort(reverse=True)

    # each cpu starts at 0 time with nothing assigned
    # heap keeps the least busy cpu at the front automatically
    heap = [(0, i, []) for i in range(num_of_cpus)]
    heapq.heapify(heap)

    for job in job_list:
        # grab whichever cpu has the most free time right now
        time, idx, processes = heapq.heappop(heap)
        # give it this job and put it back in the heap
        heapq.heappush(heap, (time + job, idx, processes + [job]))

    # put results back in cpu order for readability
    results = sorted(heap, key=lambda x: x[1])
    optimal = [processes for _, _, processes in results]

    # whoever finished last determines how long everything took
    total_time = max(time for time, _, _ in heap)

    print("Optimal Job Configuration:", optimal)
    print("Total Time:", total_time)

    return optimal, total_time

if __name__ == "__main__":
    main()