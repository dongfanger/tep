"""常考算法题"""


def test_bubble():
    """冒泡排序"""
    nums = [3, 1, 5, 2, 8]
    for i in range(len(nums)):
        # -i 是因为i个元素已经排好序了
        # -1 是因为遍历到最后防止数组越界
        for j in range(len(nums) - i - 1):
            # 把大的放后面，从小到大排序
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    print(nums)
