def sumEvenKeyedValues(sumdict):
    numbers=[]
    for i in sumdict:
         if(i%2==0):
                numbers.append(sumdict[i])
    return sum(numbers)

print(sumEvenKeyedValues({1: 2, 2: 3, 3: 4, 4: 5, 5: 6}))