#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/regular-expression-matching/


class State(object):
    """
    t = 0: Char state
    t = 1: Repeating char state
    t = 2: Inner state start
    t = 3: Inner state end
    t = 4: DFSM start
    t = 5: DFSM end
    """
    def __init__(self, t, n=None):
        """
        t: type
        n: name
        """
        self.t = t
        self.n = n
        self.trans = {}

    def add_trans(self, c, state):
        self.trans[c] = state

    def has_trans(self, c):
        return c in self.trans

    def set_t(self, t):
        self.t = t


class DFSM(object):

    def __init__(self, p):
        self.p = p
        self._build(p)

    def _build(self, p):
        stack = []

        for c in p:
            if c == '*':
                trans = stack.pop(-1)
                stat = self._repeat(trans)
                stack.append(stat)
            else:
                stack.append(c)

        s_cur = dfsm_start = State(None, 4)

        while stack:
            stat = stack.pop(0)

            if isinstance(stat, tuple):
                start, end = stat
                s_cur.add_trans('', start)

                s_cur = end
            else:
                s_cur.add_trans(stat)

                s_cur = stat

        dfsm_end = State(None, 5)
        s_cur.add_out(dfsm_end)

        self.start = dfsm_start
        self.end = dfsm_end

    def _char(self, c):
        return State(c, 0)

    def _repeat(self, c):
        repeat = State(None, 1)
        start = State(None, 2)
        end = State(None, 3)

        start.add_out(c, repeat)
        start.add_out('', end)
        repeat.add_out(c, repeat)
        repeat.add_out('', end)

        return (start, end)

    def match(self, s):
        # w_inx = s.find('.*')

        # if w_inx != -1:
        #     after_w = s[w_inx + 2:]

        # inx = 1
        # s = '^%s$' % s
        # stat = self.start.out[0]

        # while stat.t != 5:
        #     if stat.t == 0:
        #         if s[inx] == '$':
        #             return False

        #         if stat.c == '.' or stat.c == s[inx]:
        #             inx += 1
        #             stat = stat.out[0]
        #         else:
        #             return False
        #     elif stat.t == 1:
        #         if s[inx] == '$':
        #             return True

        #         if stat.c == '.' or stat.c == s[inx]:
        #             inx += 1
        #             stat = stat.out[0]
        #         else:
        #             stat = stat.out[1]
        #     elif stat.t == 2:
        #         repeat_c = stat.out[0].c

        #         if repeat_c == '.' or repeat_c == s[inx]:
        #             stat = stat.out[0]
        #         else:
        #             stat = stat.out[1]
        #     elif stat.t == 3:
        #         stat = stat.out[0]

        # if s[inx] == '$':
        #     return True
        # else:
        #     return False
        # inx = 1
        # s = '^%s$' % s
        stat = self.start.out[0]

        for c in s:
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
