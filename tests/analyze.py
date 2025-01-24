import json

with open("time2.json", "r") as fp:
    data = json.load(fp)

for id, value in data.items():
    print(f"Клиент №{id}")
    print("Время подключения:", value[0][0])

    max_sim, max_cli = 0, 0
    sum_sim, sum_cli = 0, 0
    for i in range(1, len(value)-1):
        max_sim = max(max_sim, value[i][0])
        max_cli = max(max_cli, value[i][1])

    print("Количество сообщений:", len(value)-1)
    print("Самый долгий ответ симулятора:", max_sim)
    print("Самый долгий ответ клиента:", max_cli)
    print("Среднее время ответа сиумлятора:", sum_sim / (len(value)-2))
    print("Среднее время ответа клиента:", sum_cli / (len(value)-2))
