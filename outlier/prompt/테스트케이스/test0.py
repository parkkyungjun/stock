arr와 k가 주어졌을 때, arr의 요소 중 k로 나누어 떨어지는 요소만 남기고 나머지를 제거하려고 합니다
아래 코드를 보고, 각 테스트 케이스의 결과를 예측하고 설명해줘
그리고 예외가 발생하는 경우가 있다면, 어떤 예외가 발생하는지 왜 발생했는지 설명해줘

def divide_arr(arr, k):
    answer = []
    for i in arr:
        if i % k == 0:
            answer.append(i)
    print(answer)
    return answer 

if __name__ == '__main__':
    test_cases = [
        ([7,2,5,1,5,6,6,2,3,7,8], 2),
        ([88, 63, 81, 99], 9),
        ([721, 435, 324, 8798], 0),
        (['a', 'b', 'c'], 3),
        (123, 345),
        ([1,44, None], 7),
        ([1,44, 123], 7, 456),  # Extra argument will cause an error
        ([18,48, 96], 4),
        ([567, 678, 328, 43282], -4),
        ([64.1, 23.4], 0.1)
    ]
    
    for case in test_cases:
        try:
            divide_arr(*case)
        except TypeError:
            print("Error: Invalid number of arguments passed.")


