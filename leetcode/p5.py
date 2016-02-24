#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/longest-palindromic-substring/


class Solution1(object):
    """
    This is the dynamic programming way, which exceeds the time limit of
    Leetcode online judging.
    """

    def longestPalindrome(self, chars):
        """
        :type chars: str
        :rtype: str
        """
        length = len(chars)

        if length == 0 or length == 1:
            return length

        # Prepare results memo
        memo = [[False for x in range(length)]
                for x in range(length)]

        low_inx = high_inx = -1

        for i in xrange(length):
            memo[i][i] = True
            low_inx = high_inx = i

        for i in xrange(0, length - 1):
            if chars[i] == chars[i + 1]:
                memo[i][i + 1] = True
                low_inx = i
                high_inx = i + 1

        for i in xrange(0, length - 2):
            if chars[i] == chars[i + 2]:
                memo[i][i + 2] = True
                low_inx = i
                high_inx = i + 2

        if low_inx == high_inx:
            return chars[low_inx:high_inx + 1]

        for step in xrange(3, length):
            for i in xrange(0, length - step):
                if chars[i] == chars[i + step] and \
                        memo[i + 1][i + step - 1]:
                    memo[i][i + step] = True
                    low_inx = i
                    high_inx = i + step

        return chars[low_inx:high_inx + 1]


class Solution2(object):
    """
    This one is the problem specific solution.
    The solution itself doesn't achieve a good performance
    under worst case alike 'zzzzzzzzzz...zzzz'.
    """
    def getPalindRange(self, chars, inx):
        range_low = range_high = inx
        chars_len = len(chars)

        while True:
            range_low -= 1
            range_high += 1

            if range_low <= 0 or range_high >= chars_len - 1:
                break
            if chars[range_low] != chars[range_high]:
                range_low += 1
                range_high -= 1

                break

        return (range_low, range_high + 1)

    def longestPalindrome(self, chars):
        """
        :type chars: str
        :rtype: str
        """
        chars_len = len(chars)

        if chars_len <= 1:
            return chars

        hash_chars = '#%s#' % '#'.join(chars)
        max_length = -1
        low_inx = high_inx = -1

        for inx, char in enumerate(hash_chars):
            range_low, range_high = self.getPalindRange(hash_chars, inx)
            length = range_high - range_low

            if length > max_length:
                max_length = length
                low_inx, high_inx = range_low, range_high

        return hash_chars[low_inx:high_inx].replace('#', '')


class Solution3(object):
    """
    This one is the problem specific solution with optimization.
    You can find details of the optimization here:
    http://articles.leetcode.com/longest-palindromic-substring-part-ii/
    """
    def __init__(self):
        self.memo = []

    def getPalindRange(self, chars, inx):
        range_low = range_high = inx
        chars_len = len(chars)

        while True:
            range_low -= 1
            range_high += 1

            if range_low <= 0 or range_high >= chars_len - 1:
                break
            if chars[range_low] != chars[range_high]:
                range_low += 1
                range_high -= 1

                break

        return (range_low, range_high + 1)

    def longestPalindrome(self, chars):
        """
        :type chars: str
        :rtype: str
        """
        chars_len = len(chars)

        if chars_len <= 1:
            return chars

        hash_chars = '^#%s#$' % '#'.join(chars)
        max_length = -1
        low_inx = high_inx = -1

        for inx, char in enumerate(hash_chars):
            range_low, range_high = self.getPalindRange(hash_chars, inx)
            length = range_high - range_low

            if length > max_length:
                max_length = length
                low_inx, high_inx = range_low, range_high

        return hash_chars[low_inx:high_inx].replace('#', '')
