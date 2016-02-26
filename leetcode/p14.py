#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/longest-common-prefix/


class Solution(object):

    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ''

        shortest_str = strs[0]
        shortest_len = len(shortest_str)

        for s in strs:
            s_len = len(s)
            if s_len < shortest_len:
                shortest_str = s
                shortest_len = s_len

        max_inx = -1

        for inx, char in enumerate(shortest_str):
            match = True

            for s in strs:
                if s[inx] != char:
                    match = False
                    break

            if not match:
                break
            else:
                max_inx = inx

        return shortest_str[:max_inx + 1]
