import heapq
import math

from PyQt5.QtWidgets import QTableWidget





# def heuristic(a, b):
#     (x1, y1) = a
#     (x2, y2) = b
#     return math.sqrt(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2))
#
#
# def astar(start_coordinatess: tuple, goal_coordinates: tuple,
#           gameboard: QTableWidget):
#
#     frontier = PQueue()
#     frontier.put(start_coordinatess, 0)
#     came_from = {start_coordinatess: None}
#     cost_so_far = {start_coordinatess: 0}
#
#     while not frontier.empty():
#         current = frontier.get()
#
#         if current == goal_coordinates:
#             break
#
#         for next_item in neighbors(current, gameboard):
#             new_cost = cost_so_far[current] - 1
#
#             if next_item not in cost_so_far \
#                     or new_cost > cost_so_far[next_item]:
#                 cost_so_far[next_item] = new_cost
#                 priority = new_cost + heuristic(goal_coordinates, next_item)
#                 frontier.put(next_item, priority)
#                 came_from[next_item] = current
#
#     return came_from
#
#
# def neighbors(coordinates: tuple, gameboard: QTableWidget):
#     directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
#     result = []
#
#     for direction in directions:
#         neighbor = (coordinates[0] + direction[0],
#                     coordinates[1] + direction[1])
#
#         if 0 <= neighbor[0] <= gameboard.rowCount() and \
#                 0 <= neighbor[1] <= gameboard.columnCount():
#             if gameboard.is_passable(neighbor[0], neighbor[1]):
#                 result.append(neighbor)
#
#     return result
