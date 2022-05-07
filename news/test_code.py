# from _csv import reader
# from datetime import datetime
#
# now = datetime.now()
# print(now)
#
#
# with open('static/files/data.csv', 'r', encoding='utf-8-sig') as f:
#     csv_reader = reader(f, delimiter=";")
#     for row in csv_reader:
#         print(row)


# from functools import wraps
#
#
# def decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         return result + 1
#     return wrapper
#
#
# @decorator
# def some_func():
#     return 1
#
#
# print(some_func())

