schedule = [('Taekwondo', 'Women +67 kg Gold Medal Contest', '27 July 2021 - 11:00:00', '27 July 2021 - 14:30:00'), ('Taekwondo', 'Men +80 kg Victory Ceremony', '27 July 2021 - 11:00:00', '27 July 2021 - 14:30:00'), ('Taekwondo', 'Women -49 kg Semifinals (2 matches)', '24 July 2021 - 02:00:00', '24 July 2021 - 09:00:00')]
index = 0
for i in schedule:
    i = list(i)
    index = index + 1
    print(index, i[1],"\nBegins at: ", i[2], "\nEnds at: ", i[3], "\n")