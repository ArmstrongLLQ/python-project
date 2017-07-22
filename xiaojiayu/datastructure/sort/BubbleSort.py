'''
冒泡排序法
'''
__author = 'Armstrong'

def BubbleSort(sort_list):
    list2 = sort_list
    n = list2.__len__()
    for i in range(n):
        for j in range(i+1,n):
            if list2[i] < list2[j]:
                temp = list2[i]
                list2[i] = list2[j]
                list2[j] = temp
    return list2


if __name__ == '__main__':
    sort_list = [1,3,4,6,7,8,2,4,1,2,4,1]
    print(BubbleSort(sort_list))
