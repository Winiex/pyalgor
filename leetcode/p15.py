#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/3sum/


class Solution(object):
    """
    Brute force solution. Time limit exceeded.
    """
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        memo = {}
        nums_len = len(nums)

        for inx, num in enumerate(nums):
            for inner_inx in xrange(inx + 1, nums_len):
                num1, num2 = nums[inx], nums[inner_inx]

                if num1 > num2:
                    num1, num2 = num2, num1

                value = num1 + num2

                if value in memo:
                    memo[value].append((num1, num2))
                else:
                    memo[value] = [(num1, num2)]

        results = {}

        for inx, num in enumerate(nums):
            reverse_num = -num

            if reverse_num in memo:
                for pair in memo[reverse_num]:
                    if inx in pair:
                        continue

                    a = num
                    b = pair[0]
                    c = pair[1]

                    if a > b:
                        if c < b:
                            a, b, c = c, b, a
                        elif b <= c < a:
                            a, b, c = b, c, a
                        else:
                            a, b, c = b, a, c
                    else:
                        if c < a:
                            a, b, c = c, a, b
                        elif a <= c < b:
                            a, b, c = a, c, b

                    results[(a, b, c)] = 1

        return results.keys()
