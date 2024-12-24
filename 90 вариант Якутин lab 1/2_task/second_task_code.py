def read_file():
    with open("./2_task/second_task.txt", encoding="utf-8") as file:
        lines =  file.readlines()
        table = []
        for line in lines:
            words = line.strip().split(" ")
            table.append(list(map(int, words)))

        return table

def first_operation(table):
    result = []

    for row in table:
        sum_numbers = 0
        for num in row:
            if num ** 2 < 100000:
                sum_numbers += abs(num)
        result.append(sum_numbers)

    return result

def second_operation(final_row):
    sum_numbers = 0

    for i in final_row:
        sum_numbers += i

    return(sum_numbers / len(final_row))


def write_to_file(final_row, average):
    with open("./2_task/second_task_result.txt", "w", encoding="utf-8") as file:
        for num in final_row:
            file.write(f"{num}\n")

        file.write(f"\n{average}")

table = read_file()
final_row = first_operation(table)
average = second_operation(final_row)
write_to_file(final_row, average)