#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/string-to-integer-atoi/


class Solution(object):

    def myAtoi(self, s):
        """
        :type str: str
        :rtype: int
        """
        s = s.strip()

        if s == '':
            return 0

        if s[0] == '-':
            neg = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]
            neg = False
        else:
            neg = False

        result = 0

        for c in s:
            try:
                ci = int(c)
            except ValueError:
                # Invalid string.
                break

            result = result * 10 + ci

        result = -result if neg else result

        if result > 2147483647:
            return 2147483647
        elif result < -2147483648:
            return -2147483648

        return result
