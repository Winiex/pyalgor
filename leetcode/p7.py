#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/reverse-integer/


class Solution(object):

    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if -10 < x < 10:
            return x

        neg = True if x < 0 else False
        num = x if x > 0 else -x

        digits = []

        while num != 0:
            digits.append(num % 10)
            num /= 10

        result = 0
        expo = 0

        while digits:
            digit = digits.pop(0)
            result = result * 10 + digit
            expo += 1

        result = -result if neg else result

        if result > 2147483647 or result < -2147483648:
            return 0

        return result
