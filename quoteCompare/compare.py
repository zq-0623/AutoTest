from deepdiff import DeepDiff

list1 = []
list2 = []
result = DeepDiff(list1, list2)
print(result.pretty())
