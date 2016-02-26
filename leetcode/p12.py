#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/integer-to-roman/


class Solution(object):

    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """
        result = []
        base = 10

        while num != 0:
            digit = num % 10

            if base == 10:
                if 0 < digit <= 3:
                    result.insert(0, digit * 'I')
                elif digit == 4:
                    result.insert(0, 'IV')
                elif digit == 5:
                    result.insert(0, 'V')
                elif 5 < digit < 9:
                    result.insert(0, 'V' + (digit - 5) * 'I')
                elif digit == 9:
                    result.insert(0, 'IX')
            elif base == 100:
                if 0 < digit <= 3:
                    result.insert(0, digit * 'X')
                elif digit == 4:
                    result.insert(0, 'XL')
                elif digit == 5:
                    result.insert(0, 'L')
                elif 5 < digit < 9:
                    result.insert(0, 'L' + (digit - 5) * 'X')
                elif digit == 9:
                    result.insert(0, 'XC')
            elif base == 1000:
                if 0 < digit <= 3:
                    result.insert(0, digit * 'C')
                elif digit == 4:
                    result.insert(0, 'CD')
                elif digit == 5:
                    result.insert(0, 'D')
                elif 5 < digit < 9:
                    result.insert(0, 'D' + (digit - 5) * 'C')
                elif digit == 9:
                    result.insert(0, 'CM')
            elif base == 10000:
                result.insert(0, digit * 'M')

            num /= 10
            base *= 10

        return ''.join(result)
