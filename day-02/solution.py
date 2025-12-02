from collections import Counter

DEBUG_INPUT: str = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
DEBUG_RESULT = 1227775554
DEBUG_RESULT_II = 4174379265

PUZZLE_INPUT: str = "16100064-16192119,2117697596-2117933551,1-21,9999936269-10000072423,1770-2452,389429-427594,46633-66991,877764826-877930156,880869-991984,18943-26512,7216-9427,825-1162,581490-647864,2736-3909,39327886-39455605,430759-454012,1178-1741,219779-244138,77641-97923,1975994465-1976192503,3486612-3602532,277-378,418-690,74704280-74781349,3915-5717,665312-740273,69386294-69487574,2176846-2268755,26-45,372340114-372408052,7996502103-7996658803,7762107-7787125,48-64,4432420-4462711,130854-178173,87-115,244511-360206,69-86"

# INPUT = DEBUG_INPUT
INPUT = PUZZLE_INPUT

def get_range_funcs(input_str: str):
    for id_range in input_str.split(","):
        start, end = map(int, id_range.split("-"))
        yield map(str, range(start, end + 1))


def is_invalid_id(value: str) -> bool:
    if value.startswith('0'):
        raise ValueError(value)
    if len(value) % 2 == 1:
        return False
    sub_value = value[0:len(value) // 2]
    return sub_value + sub_value == value


def is_invalid_id_part_ii(value: str) -> bool:
    if value.startswith('0'):
        raise ValueError(value)
    max_chunk_size = len(value) // 2
    chunks = set([
        value[i:i + size]
        for size in range(1, max_chunk_size + 1)
        for i in range(0, len(value))
    ])
    for chunk in chunks:
        for rep in range(1, len(value) + 1):
            repeat = ''.join([chunk,] * rep)
            if repeat == value:
                return True
            elif len(repeat) >= len(value):
                break
    return False


if __name__ == "__main__":
    all_invalid_ids = []
    for range_func in get_range_funcs(INPUT):
        values = list(range_func)

        start, end = values[0], values[-1]
        # invalid_ids = list(filter(is_invalid_id, values))
        invalid_ids = list(filter(is_invalid_id_part_ii, values))
        invalid_ids_str = ", ".join(invalid_ids)
        count = len(invalid_ids)
        message = f"{start}-{end} has {count} invalid IDs, {invalid_ids_str}."
        print(message)

        all_invalid_ids.extend(invalid_ids)

    invalid_id_sum = sum(map(int, all_invalid_ids))
    print(f"sum of invalid ids: {invalid_id_sum}")
    # assert invalid_id_sum == DEBUG_RESULT_II

