# -*- coding:utf-8 -*-
"""
Longest palindromic substring.

http://articles.leetcode.com/longest-palindromic-substring-part-i/
"""


def dp(chars):
    """
    The dynamic programming solution.
    """
    length = len(chars)

    if length == 0 or length == 1:
        return length

    # Prepare results memo
    memo = [[False for x in range(length)]
            for x in range(length)]

    longest_length = 1

    for i in xrange(length):
        memo[i][i] = True

    for i in xrange(0, length - 1):
        if chars[i] == chars[i + 1]:
            memo[i][i + 1] = True
            longest_length = 2

    for i in xrange(0, length - 2):
        if chars[i] == chars[i + 2]:
            memo[i][i + 2] = True
            longest_length = 3

    if longest_length == 1:
        return 1

    for step in xrange(3, length):
        for i in xrange(0, length - step):
            if chars[i] == chars[i + step] and \
                    memo[i + 1][i + step - 1]:
                memo[i][i + step] = True
                longest_length = step + 1

    return longest_length


def specific(chars):
    """
    The problem specific solution.
    """
