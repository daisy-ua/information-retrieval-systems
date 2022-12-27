def common_elements(list1, list2):
    res = list(set(list1).intersection(list2))
    res.sort()
    return res
