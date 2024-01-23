import time


class Base(object):
    def __init__(self, node_num: int = 12) -> None:
        self.node_num = node_num

    def nodes_mapping(self, node_in, node_out) -> int:
        """Maps node connection to index which can be use to get proposed paths"""
        node_max_conn = self.node_num - 1
        idx = node_in * node_max_conn + node_out
        return idx

    @staticmethod
    def choose_slots_num(distance: int, bitrate: int) -> int:
        """Returns number of slots needed for demand"""
        slots_num = 0

        if bitrate <= 200:
            slots_num = 6
        elif 200 < bitrate and bitrate <= 400:
            if distance <= 800:
                slots_num = 6
            else:
                slots_num = 9
        elif 400 < bitrate and bitrate <= 600:
            if distance <= 1600:
                slots_num = 9
        elif 600 < bitrate and bitrate <= 800:
            if distance <= 200:
                slots_num = 9

        return slots_num

    @staticmethod
    def measure_execution_time(func):
        """Measures execution time of function which is decorated"""

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            text = f"Execution time of {func.__name__}: {execution_time} seconds"
            with open("wyniki_pomiaru_czasu.txt", "a") as file:
                file.write(text)
            return result

        return wrapper
