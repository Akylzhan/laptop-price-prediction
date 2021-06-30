# CHECK integrated+discrete gpus

import pandas as pd

data = pd.read_json("data/laptops.json", orient="index")
data.index.name = "name"

data.rename(columns={"видеокарта": "gpu",
                     "процессор": "cpu",
                     "тип жесткого диска": "storage type",
                     "размер оперативной памяти": "ram",
                     "общий объем накопителей": "storage size",
                     "разрешение экрана": "screen resolution",
                     "диагональ экрана": "screen diagonal"},
            inplace=True)

data.reset_index(inplace=True)

data.at[125, 'cpu'] = "Intel Core i5 1135G7"
data.at[232, 'cpu'] = "Intel Core i7 1165G7"
data.at[232, 'gpu'] = "Intel Iris Xe Graphics"
data.at[70, 'gpu'] = "Intel Iris Xe Graphics"

data.at[269, 'cpu'] = "Intel Pentium Gold 7505"

data.at[615, 'cpu'] = "Intel Core i5 8265U"
data.at[167, 'cpu'] = "Intel Core i5 8265U"

data.at[128, 'cpu'] = "Intel Core i3 7020U"
data.at[533, 'cpu'] = "Intel Core i7 10870H"

data.at[11, 'gpu'] = "Intel UHD Graphics 600"
data.at[22, 'gpu'] = "Intel UHD Graphics"
data.at[80, 'gpu'] = "Intel UHD Graphics"
data.at[82, 'gpu'] = "Intel UHD Graphics 600"
data.at[36, 'gpu'] = "Intel UHD Graphics 600"

data['cpu'] = data['cpu'].str.replace('-', ' ')


def rename(data, column, substr, name):
    mask1 = data[column].str.contains(substr)
    mask2 = data[column] == name

    for i in data[(mask1) & (~mask2)].index:
        data.at[i, column] = name


rename_pairs = [
    ("8250U", "Intel Core i3 8250U"),
    ("1135G7", "Intel Core i5 1135G7"),
    ("1035G1", "Intel Core i5 1035G1"),
    ("1165G7", "Intel Core i7 1165G7"),
    ("10750H", "Intel Core i7 10750H"),
    ("9750H", "Intel Core i7 9750H"),
    ("1005G1", "Intel Core i3 1005G1"),
    ("1115G4", "Intel Core i3 1115G4"),

    ("N5000", "Intel Pentium Silver N5000"),
    ("N5030", "Intel Pentium Silver N5030"),
    ("N4120", "Intel Celeron N4120"),

    ("3020e", "AMD Athlon 3020e"),
    ("3050U", "AMD Athlon Silver 3050U"),
    ("3150U", "AMD Athlon Gold 3150U"),
    ("9120", "AMD A4 9120e"),
    ("9220", "AMD A6 9220e"),
    ("9225", "AMD A6 9225"),
    ("3250U", "AMD Ryzen 3 3250U"),
    ("5800HS", "AMD Ryzen 7 5800HS"),
    ("4700U", "AMD Ryzen 7 4700U"),
    ("4800H", "AMD Ryzen 7 4800H"),
    ("5900HX", "AMD Ryzen 9 5900HX"),
]

for substr, name in rename_pairs:
    rename(data, "cpu", substr, name)


mask1 = data['cpu'].str.contains("Core")
mask2 = data['cpu'].str.contains("Pentium")
mask3 = ~data['cpu'].str.contains("Intel")
indexes = data[(mask1 | mask2) & mask3].index
for i in indexes:
    data.at[i, "cpu"] = "Intel " + data.loc[i, "cpu"]


data.dropna(inplace=True)

data['gpu'] = data['gpu'].str.replace('встроенная ', '')
data['gpu'] = data['gpu'].str.replace('видеокарта ', '')
data['gpu'] = data['gpu'].str.replace('дискретная ', '')
data['gpu'] = data['gpu'].str.replace('Nvidia', 'NVIDIA')
data['gpu'] = data['gpu'].str.replace('NVidia', 'NVIDIA')
data['gpu'] = data['gpu'].str.replace('nVidia', 'NVIDIA')
data['gpu'] = data['gpu'].str.replace('NVIDEA', 'NVIDIA')

data['gpu'] = data['gpu'].str.strip()

for i in [197, 201, 235, 238, 242, 243, 285, 303, 379, 395, 406]:
    data.at[i, "gpu"] = "Intel Iris Xe Graphics"

rename(data, "gpu", "видеокарта, ", "Intel HD Graphics 400")
rename(data, "gpu", "600", "Intel UHD Graphics 600")
rename(data, "gpu", "Iris Xe Max", "Intel Iris Xe Max")
rename(data, "gpu", "R3", "AMD Radeon R3")
rename(data, "gpu", "R4", "AMD Radeon R4")
rename(data, "gpu", "Vega 3", "AMD Radeon RX Vega 3")
rename(data, "gpu", "Vega 8", "AMD Radeon RX Vega 8")
rename(data, "gpu", "Vega 6", "AMD Radeon RX Vega 6")
rename(data, "gpu", "Vega 10", "AMD Radeon RX Vega 10")

rename(data, "gpu", "M1", "Apple M1")
rename(data, "gpu", "Neural", "Apple M1")

rename(data, "gpu", "110", "NVIDIA GeForce MX110")
rename(data, "gpu", "230", "NVIDIA GeForce MX230")
rename(data, "gpu", "330", "NVIDIA GeForce MX330")
rename(data, "gpu", "350", "NVIDIA GeForce MX350")
rename(data, "gpu", "1650Ti", "NVIDIA GeForce GTX 1650 Ti")
rename(data, "gpu", "1660Ti", "NVIDIA GeForce GTX 1660 Ti")
rename(data, "gpu", "Ti 6Gb", "NVIDIA GeForce GTX 1660 Ti")
rename(data, "gpu", "GTX1650", "NVIDIA GeForce GTX 1650")
rename(data, "gpu", "GeForce GeForce", "NVIDIA GeForce GTX 1650")
rename(data, "gpu", "3050Ti", "NVIDIA GeForce RTX 3050 Ti")

mask1 = data['gpu'].str.contains("GeForce")
mask2 = ~data['gpu'].str.contains("idia")
mask3 = ~data['gpu'].str.contains("NV")
indexes = data[mask1 & mask2 & mask3].index
for i in indexes:
    data.at[i, "gpu"] = "NVIDIA " + data.loc[i,"gpu"]

mask1 = data['gpu'].str.contains("Plus")
mask2 = ~data['gpu'].str.contains("Graphics")
indexes = data[mask1 & mask2].index
for i in indexes:
    data.at[i, "gpu"] = "Intel Iris Plus Graphics"


data.at[169, "name"] = "ASUS " + data.loc[169, "name"]
data["name"] = data["name"].str.replace("LENOVO", "Lenovo")
data["name"] = data["name"].str.replace("DELL", "Dell")
data["name"] = data["name"].str.replace("ASUS", "Asus")


data.to_csv("data/laptops_clean.csv", index=False)