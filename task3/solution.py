def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Возвращает общее время (в секундах), в течение которого ученик и преподаватель
    одновременно присутствовали на уроке.

    :param intervals: словарь с keys 'lesson', 'pupil', 'tutor', values списки таймстемпов
    :return: int - длительность общего присутствия в секундах
    """

    def to_intervals(timestamps: list) -> list[tuple]:
        return [(timestamps[i], timestamps[i + 1]) for i in range(0, len(timestamps), 2)]

    def clip_to_lesson(intervals: list[tuple], lesson_start: int, lesson_end: int) -> list[tuple]:
        clipped = []
        for start, end in intervals:
            if end <= lesson_start or start >= lesson_end:
                continue
            clipped.append((max(start, lesson_start), min(end, lesson_end)))
        return clipped

    def merge_intervals(intervals: list[tuple]) -> list[tuple]:
        if not intervals:
            return []
        intervals.sort()
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))
        return merged

    def intersect(a: list, b: list) -> list[tuple]:
        i = j = 0
        result = []
        while i < len(a) and j < len(b):
            start_a, end_a = a[i]
            start_b, end_b = b[j]
            start = max(start_a, start_b)
            end = min(end_a, end_b)
            if start < end:
                result.append((start, end))
            if end_a < end_b:
                i += 1
            else:
                j += 1
        return result

    lesson_start, lesson_end = intervals["lesson"]

    pupil_intervals = to_intervals(intervals["pupil"])
    tutor_intervals = to_intervals(intervals["tutor"])

    pupil_intervals = merge_intervals(clip_to_lesson(pupil_intervals, lesson_start, lesson_end))
    tutor_intervals = merge_intervals(clip_to_lesson(tutor_intervals, lesson_start, lesson_end))

    common = intersect(pupil_intervals, tutor_intervals)

    return sum(end - start for start, end in common)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
