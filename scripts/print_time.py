# defining a function return the current time 

import time


def show_time():
	return time.ctime()


if __name__ == '__main__':
	print(show_time())
