"""
prompt: 
try except를 매번 입력하지 말고 함수의 입력을 list로 가지고
for문을 돌려서 처리하도록 수정해줘

그리고 divide_arr 함수의 나누기 처리를
answer에 추가하는 형태가 아니라
컴프리헨션 방법으로 리스트를 만들어서
바로 리턴할 수 있도록 해줘
"""

def divide_arr(arr, k):
    answer = []
    for i in arr:
        if i % k == 0:
            answer.append(i)
    return answer 

if __name__ == '__main__':
    try:
        print(divide_arr([7,2,5,1,5,6,6,2,3,7,8], 2))
    except TypeError:
        print("Error: Invalid number of arguments passed.")
    
    try:
        print(divide_arr([88, 63, 81, 99], 9))
    except TypeError:
        print("Error: Invalid number of arguments passed.")
    
    try:
        print(divide_arr([721, 435, 324, 8798], 0))
    except TypeError:
        print("Error: Invalid number of arguments passed.")
    
    try:
        print(divide_arr(['a', 'b', 'c'], 3))
    except TypeError:
        print("Error: Invalid number of arguments passed.")
    
    try:
        print(divide_arr(123, 345))
    except TypeError:
        print("Error: Invalid number of arguments passed.")
