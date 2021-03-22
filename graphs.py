from matplotlib import pyplot as plt

SEQUENTIAL_PC_TIME_MEASURE = 10
SEQUENTIAL_SERVER_TIME_MEASURE = 8
GRID_SEARCH_TIME_MEASURE = 4

plt.figure(figsize=[20, 12])
x = list(range(3))
y = [SEQUENTIAL_PC_TIME_MEASURE, SEQUENTIAL_SERVER_TIME_MEASURE, GRID_SEARCH_TIME_MEASURE]
plt.xticks(x, ['Personal Computer', 'Standalone Server', 'Multi Server'])
plt.xlabel("Type of worker")
plt.ylabel("Time to search (sec)")
plt.bar(x, y)
plt.show()
