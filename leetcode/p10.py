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

    def __repr__(self):
        return '<State t: %s, n:%s>' % (self.t, self.n)


class DFSM(object):

    def __init__(self, p):
        self.p = p
        self.stat_count = 0
        self._build(p)

    def _new_state(self, t):
        self.stat_count += 1
        return State(t, self.stat_count)

    def _zero_char_stats(self, stat):
        z_stats = []
        stats = [stat]

        while stats:
            stat = stats.pop(0)

            for trans, to_stat in stat.trans.items():
                if trans == '':
                    z_stats.append(to_stat)
                    stats.append(to_stat)

        return z_stats

    def _build(self, p):
        stack = []
        dfsm_start = self._new_state(4)

        if p == '':
            dfsm_end = self._new_state(5)
            stat = self._new_state(0)
            dfsm_start.add_trans('^', stat)
            stat.add_trans('$', dfsm_end)
            self.start = dfsm_start
            self.end = dfsm_end

            return

        for c in p:
            if c == '*':
                start, _ = stack.pop(-1)
                repeat_c = start.trans.keys()[0]
                stat = self._repeat(repeat_c)
            else:
                stat = self._char(c)

            stack.append(stat)

        s_cur, e_cur = stack.pop(0)
        dfsm_start.add_trans('^', s_cur)

        while stack:
            start, end = stack.pop(0)

            if len(s_cur.trans) == 1:
                trans_c = s_cur.trans.keys()[0]
                s_cur.trans[trans_c] = start
            elif len(s_cur.trans) == 2:
                repeat_c = s_cur.trans.keys()[0]
                repeat_s = s_cur.trans[repeat_c]

                repeat_s.trans[''] = start
                s_cur.trans[''] = start

            s_cur = start
            e_cur = end

        dfsm_end = self._new_state(5)
        e_cur.add_trans('$', dfsm_end)

        self.start = dfsm_start
        self.end = dfsm_end

    def _char(self, c):
        start = self._new_state(2)
        end = self._new_state(3)

        start.add_trans(c, end)

        return (start, end)

    def _repeat(self, c):
        repeat = self._new_state(1)
        start = self._new_state(2)
        end = self._new_state(3)

        start.add_trans(c, repeat)
        start.add_trans('', end)
        repeat.add_trans(c, repeat)
        repeat.add_trans('', end)

        return (start, end)

    def match(self, s):
        # Running states.
        s = '^%s$' % s
        next_stats = []
        stats = [self.start]

        for c in s:
            for stat in stats:
                for trans_c, to_stat in stat.trans.items():
                    if trans_c == '.' or trans_c == c:
                        next_stats.append(to_stat)
                        next_stats += self._zero_char_stats(to_stat)

            stats = next_stats
            next_stats = []

        match = False

        for stat in stats:
            if stat.t == 5:
                match = True

        return match


class Solution1(object):
    """
    The solution based on state mathine theory.
    Unfortunately, it exceeds the time limit.
    """
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        dfsm = DFSM(p)
        return dfsm.match(s)


class Solution2(object):
    """
    The dynamic programming solution, recursively.
    """
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        s_len = len(s)
        p_len = len(p)

        s_inx = 1
        p_inx = 1

        memo = [[i for i in xrange(p_len)]
                for j in s_len]
        # Pattern '' matches string ''.
        memo[0][0] = True

        while s_inx < s_len:
            while p_inx < p_len:
                p_char = p[p_inx]

                if p_char == '*':
                    pass
                else:
                    if memo[s_inx - 1][p_inx - 1]:
                        pass
                    else:
                        pass
                    if p_char == '.' and memo[s_inx - 1][p_inx - 1]:
                        memo[s_inx][p_inx] = True
                p_inx += 1
            s_inx += 1
