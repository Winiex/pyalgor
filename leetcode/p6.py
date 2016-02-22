#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/zigzag-conversion/
import math


class Solution(object):

    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1:
            return s

        if numRows == 2:
            return s[0::2] + s[1::2]

        s_len = len(s)
        group_len = 2 * numRows - 2
        groups_count = int(math.ceil(s_len / float(group_len)))

        result = []

        for step in xrange((group_len / 2) + 1):
            for group in xrange(groups_count):
                group_begin = group * group_len

                if step == 0:
                    result.append(s[group_begin])
                elif step == group_len / 2:
                    char_inx = group_begin + step

                    if char_inx < s_len:
                        result.append(s[group_begin + step])
                else:
                    char1_inx = group_begin + step

                    if char1_inx < s_len:
                        result.append(s[char1_inx])

                    char2_inx = group_begin + (group_len - step)

                    if char2_inx < s_len:
                        result.append(s[char2_inx])

        return ''.join(result)
