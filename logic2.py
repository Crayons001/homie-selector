import random

guys = ["Cecil", "Hargine", "Caleb", "Phil", "Johnmark", "Immanuel"]
girls = ["Fiona", "Yvonne", "Ericah", "Stacey", "Phoebe", "Gloria"]

random.shuffle(guys)
random.shuffle(girls)

combined = list(zip(guys, girls))

print(combined)
