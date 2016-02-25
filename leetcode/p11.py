#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/container-with-most-water/


class Solution1(object):
    """
    The dynamic programming way. It's not so efficient.
    """
    def maxArea(self, lines):
        """
        :type lines: List[int]
        :rtype: int
        """
        l_len = len(lines)
        memo = [[0 for x in xrange(l_len)]
                for x in xrange(l_len)]

        max_water = 0

        for l_inx in xrange(l_len - 1):
            for r_inx in xrange(l_inx + 1, l_len):
                part_max = 0

                for inner_inx in xrange(l_inx, r_inx):
                    tmp_len = r_inx - inner_inx
                    tmp_water = lines[r_inx] * tmp_len \
                        if lines[r_inx] < lines[inner_inx] \
                        else lines[inner_inx] * tmp_len

                    if tmp_water > part_max:
                        part_max = tmp_water

                part_max = max(part_max, memo[l_inx][r_inx - 1])
                memo[l_inx][r_inx] = part_max

                if part_max > max_water:
                    max_water = part_max

        return max_water


class Solution2(object):
    """
    The problem specific way.
    """
    def maxArea(self, lines):
        """
        :type lines: List[int]
        :rtype: int
        """
