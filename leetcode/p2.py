#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode.com/problems/add-two-numbers/


class ListNode(object):

    def __init__(self, val):
        self.val = val
        self.next = None


class Solution(object):

    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        node1 = l1
        node2 = l2

        node = s_node = ListNode(-1)

        sum = 0

        while node1 is not None or \
                node2 is not None:
            sum /= 10

            if node1 is not None:
                sum += node1.val
                node1 = node1.next

            if node2 is not None:
                sum += node2.val
                node2 = node2.next

            node.next = ListNode(sum % 10)
            node = node.next

        if sum / 10 == 1:
            node.next = ListNode(1)

        return s_node.next
