class Base(object):
    @staticmethod
    def choose_slots_num(distance: int, bitrate: int) -> int:
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