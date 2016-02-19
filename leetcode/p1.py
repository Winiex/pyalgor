#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/two-sum/


class Solution1(object):

    def twoSum(self, nums, target):
        length = len(nums)
        for outter_i in xrange(length):
            first_num = nums[outter_i]
            remain = target - first_num

            for inner_i in xrange(outter_i + 1, length):
                second_num = nums[inner_i]

                if second_num == remain:
                    return [outter_i, inner_i]


class Solution2(object):

    def twoSum(self, nums, target):
        d = {}
        for inx, val in enumerate(nums):
            remain = target - val

            if remain in d:
                return [d[remain], inx]
            else:
                d[val] = inx
