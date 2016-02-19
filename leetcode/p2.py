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

        result = node1.val + node2.val

        if result >= 10:
            carry = 1
            result = result - 10
        else:
            carry = 0

        node = result_node = ListNode(result)
        node1 = node1.next
        node2 = node2.next

        while node1 is not None and \
                node2 is not None:
            result = node1.val + node2.val + carry

            if result >= 10:
                carry = 1
                result = result - 10
            else:
                carry = 0

            node.next = ListNode(result)
            node = node.next

            node1 = node1.next
            node2 = node2.next

        if node1 is None:
            while node2 is not None:
                result = node2.val + carry

                if result >= 10:
                    carry = 1
                    result = result - 10
                else:
                    carry = 0

                node.next = ListNode(result)
                node = node.next

                node2 = node2.next
        elif node2 is None:
            while node1 is not None:
                result = node1.val + carry

                if result >= 10:
                    carry = 1
                    result = result - 10
                else:
                    carry = 0

                node.next = ListNode(result)
                node = node.next

                node1 = node1.next

        if carry != 0:
            node.next = ListNode(carry)

        return result_node
