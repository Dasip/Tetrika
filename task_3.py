def appearance(intervals):
    lesson_start = intervals['lesson'][0]
    lesson_end = intervals['lesson'][1]

    pupil_cursor = 0
    tutor_cursor = 0
    pupil_link = intervals["pupil"]
    tutor_link = intervals["tutor"]
    shared_time = 0
    latest_end = lesson_start

    while True:
        # достигли последнего интервала активности ученика
        if pupil_cursor == len(pupil_link):
            break

        # достигли последнего интервала активности тьютора
        if tutor_cursor == len(tutor_link):
            break

        # Пропускаем интервал ученика, если он находится внутри другого интервала
        if pupil_link[pupil_cursor+1] < latest_end:
            pupil_cursor += 2
            continue

        # интервал активности ученика после окончания урока
        if pupil_link[pupil_cursor] > lesson_end:
            break

        # интервал активности тьютора после окончания урока
        if tutor_link[tutor_cursor] > lesson_end:
            break

        # интервал активности ученика до начала урока
        if pupil_link[pupil_cursor+1] < lesson_start:
            pupil_cursor += 2
            continue

        # интервал активности тьютора до начала урока
        if tutor_link[tutor_cursor+1] < lesson_start:
            tutor_cursor += 2
            continue

        # Обрезаем интервалы ученика и тьютора рамками урока
        pupil_link[pupil_cursor] = max(lesson_start, pupil_link[pupil_cursor])
        pupil_link[pupil_cursor+1] = min(lesson_end, pupil_link[pupil_cursor+1])

        tutor_link[tutor_cursor] = max(lesson_start, tutor_link[tutor_cursor])
        tutor_link[tutor_cursor+1] = min(lesson_end, tutor_link[tutor_cursor+1])

        # Ученик зашел позже, чем вышел тьютор
        if pupil_link[pupil_cursor] > tutor_link[tutor_cursor+1]:
            latest_end = pupil_link[pupil_cursor]
            tutor_cursor += 2

        # Ученик вышел раньше, чем зашел тьютор
        elif pupil_link[pupil_cursor+1] < tutor_link[tutor_cursor]:
            latest_end = pupil_link[pupil_cursor+1]
            pupil_cursor += 2

        else:
            # Обрезаем интервал ученика, если он начинается внутри другого его интервала
            if pupil_link[pupil_cursor] < latest_end:
                pupil_link[pupil_cursor] = latest_end

            latest_end = min(pupil_link[pupil_cursor + 1], tutor_link[tutor_cursor+1])

            shared_time += (min(tutor_link[tutor_cursor+1], pupil_link[pupil_cursor+1]) -
                            max(tutor_link[tutor_cursor], pupil_link[pupil_cursor]))

            if pupil_link[pupil_cursor+1] > tutor_link[tutor_cursor+1]:
                tutor_cursor += 2
            else:
                pupil_cursor += 2

    return shared_time


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500,  # +1700 (1700) OK
                        1594702807, 1594704542,  # +42 (1742) OK
                        1594704512, 1594704513,  # Excluded (1742) OK
                        1594704564, 1594705150,  # +586
                        1594704581, 1594704582,  # Excluded
                        1594704734, 1594705009,  # Excluded
                        1594705095, 1594705096,  # Excluded
                        1594705106, 1594706480,  # + 1250
                        1594705158, 1594705773,  # Excluded
                        1594705849, 1594706480,  # Excluded
                        1594706500, 1594706875,  # Excluded
                        1594706502, 1594706503,  # Excluded
                        1594706524, 1594706524,  # Excluded
                        1594706579, 1594706641],  # Excluded

              'tutor': [1594700035, 1594700364,  # Excluded OK
                        1594702749, 1594705148,  # OK
                        1594705149, 1594706463]}, # OK
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
