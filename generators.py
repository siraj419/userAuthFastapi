
def count(init, end):
    counts = []
    for n in range(init, end+1):
        counts.append(n)
    return counts

def count_generator(init, end):
    for n in range(init, end+1):
        yield n

genartor = count_generator(1, 1000)
print(genartor)

# print(next(genartor))
# print(next(genartor))
# print(next(genartor))
# print(next(genartor))
# print(next(genartor))

# for num in count_generator(1, 1000):
#     print(num)

# print(count_generator(1, 1000))