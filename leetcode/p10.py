#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/regular-expression-matching/


class State(object):
    """
    t = 0: Char state
    t = 1: DFSM start
    t = 2: DFSM end
    t = 3: Inner state start
    t = 4: Inner state end
    t = 5: Wildchar state
    """
    def __init__(self, c, t=0):
        self.c = c
        self.t = t
        self.out = []

    def add_out(self, state):
        self.out.append(state)


class DFSM(object):

    def __init__(self, p):
        self._build(p)

    def _build(self, p):
        stack = []

        for c in p:
            if c == '*':
                c_stat = stack.pop(-1)
                stat = self._char_repeat(c_stat)
            elif c == '.':
                stat = self._wildchar()
            else:
                stat = self._char(c)

            stack.append(stat)

    def _char(self, c):
        return State(c)

    def _char_repeat(self, c_stat):
        pass

    def _wildchar(self):
        pass

    def match(self, s):
        pass


class Solution(object):

    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        dfsm = DFSM(p)
        return dfsm.match(s)
