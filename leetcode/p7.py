#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/reverse-integer/
import math


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
            digit = digits.pop(-1)
            result += digit * int(math.pow(10, expo))
            expo += 1

        result = -result if neg else result

        if result > 2147483647:
            return 0

        return result
