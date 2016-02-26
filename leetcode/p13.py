#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/roman-to-integer/


class Solution(object):

    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        values = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
        }

        stack = []

        for c in s:
            value = values[c]

            if stack:
                former_value = stack[-1]
                if former_value < value:
                    value -= former_value
                    stack[-1] = value
                else:
                    stack.append(value)
            else:
                stack.append(value)

        return sum(stack)
