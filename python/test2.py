# def is_valid(s, k, n):
#   return len(s) == k and sum(s) == n

# def is_bad(s, k, n):
#   sum_s = sum(s)
#   len_s = len(s)
#   return len(s) > k or sum_s > n or (len_s == k and sum_s != n)

# def search(solutions, digits, s, k, n):
#   if is_valid(s, k, n):
#     solutions.append(s.copy())
  
#   for d in digits:
#     s.append(d)
#     if not is_bad(s, k, n):
#       search(solutions, set(digits) - set([d]), s, k, n)
#     s.pop()
  
# class Solution:
#   def combinationSum3(self, k, n):
#     solutions = []
#     digits = range(1, 10)
#     s = []
#     search(solutions, digits, s, k, n)
#     return solutions
  
# print(Solution().combinationSum3(3, 7))

def getCandidates(nums):
  candidates = []
  toPick = set(nums)
  for num in toPick:
    newNums = nums.copy()
    newNums.remove(num)
    candidates.append((num, newNums))
  return candidates

def search(solutions, nums, s):
  if not nums:
    solutions.append(s.copy())
  else:
    for c, otherNums in getCandidates(nums):
      # print(c, otherNums)
      s.append(c)
      search(solutions, otherNums, s)
      s.pop()
        
def permuteUnique(nums):
  solutions = []
  search(solutions, nums, [])
  return solutions

print(permuteUnique([1,1,2]))