#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/3sum/


class Solution1(object):
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
                value = nums[inx] + nums[inner_inx]

                if value in memo:
                    memo[value].append((inx, inner_inx))
                else:
                    memo[value] = [(inx, inner_inx)]

        results = {}

        for inx, num in enumerate(nums):
            reverse_num = -num

            if reverse_num in memo:
                for pair in memo[reverse_num]:
                    if inx in pair:
                        continue

                    a = num
                    b = nums[pair[0]]
                    c = nums[pair[1]]

                    results[tuple(sorted([a, b, c]))] = 1

        return results.keys()
