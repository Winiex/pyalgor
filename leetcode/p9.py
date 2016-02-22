#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/palindrome-number/


class Solution(object):

    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False

        if 0 <= x < 10:
            return True

        if 11 <= x < 100:
            return x % 11 == 0

        low_base = 10
        high_base = 10

        while x / high_base != 0:
            high_base *= 10

        high_base /= 10

        while True:
            if high_base == 1:
                return True

            h_num = (x - (x % high_base)) / high_base
            l_num = x % low_base

            if high_base == 10:
                if h_num == l_num:
                    return True

            if h_num != l_num:
                return False

            x = (x - h_num * high_base) / 10
            high_base /= 100
