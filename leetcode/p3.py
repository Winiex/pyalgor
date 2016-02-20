#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/longest-substring-without-repeating-characters/


class Solution(object):

    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        s_len = len(s)
        if s_len <= 1:
            return s_len

        table = {}
        max_length = -1
        tmp_length = 0
        start = 0

        for inx, char in enumerate(s):
            if char in table:
                former_inx = table[char]
                table[char] = inx

                if former_inx < start:
                    tmp_length += 1
                else:
                    start = former_inx + 1
                    tmp_length = inx - start + 1
            else:
                table[char] = inx
                tmp_length += 1

            if tmp_length > max_length:
                max_length = tmp_length

        return max_length
