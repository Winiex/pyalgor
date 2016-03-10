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
        nums_len = len(nums)
        sorted_nums = sorted(nums)
        results = {}

        for l_inx, num in enumerate(sorted_nums):
            m_inx = l_inx + 1
            r_inx = nums_len - 1

            while m_inx < r_inx:
                sum_result = sorted_nums[l_inx] + \
                    sorted_nums[m_inx] + \
                    sorted_nums[r_inx]

                if sum_result > 0:
                    r_inx -= 1
                elif sum_result < 0:
                    m_inx += 1
                else:
                    triple = (
                        sorted_nums[l_inx],
                        sorted_nums[m_inx],
                        sorted_nums[r_inx]
                    )

                    results[triple] = True
                    m_inx += 1
                    r_inx -= 1

        return results.keys()
