"""
Wielu z nas na pulpicie ma folder o nazwie "Do przejrzenia", 
do którego wrzucamy na bieżąco randomowe rzeczy, ale nigdy nie mamy czasu, 
aby w końcu ten folder "przejrzeć" i zrobić porządek.

Napiszemy skrypt, który wreszcie zrobi porządek w tym folderze. 
Ostatecznie będziesz mógł dostosować ten program do swoich potrzeb tak, 
aby realizował indywidualny scenariusz odpowiadający Twoim wymaganiom. 
W tym celu nasza aplikacja będzie sprawdzać rozszerzenie pliku 
(ostatnie znaki w nazwie pliku, zwykle po kropce) i na podstawie rozszerzenia podejmować decyzję, 
do jakiej kategorii należy ten plik.

Przy uruchomieniu skrypt przyjmuje jeden argument - jest to nazwa folderu, 
w którym będzie przeprowadzał sortowanie. Przyjmując, że plik z programem nazywa się `sort.py`, 
aby posortować folder `/user/Desktop/Bałagan`, należy uruchomić skrypt za pomocą polecenia 
`python sort.py /user/Desktop/Bałagan`.

Stworzenie osobnej funkcji do przetwarzania folderu na pewno ułatwi Ci pomyślne wykonanie tego zadania.
Funkcja przetwarzania folderów powinna rekurencyjnie wywoływać samą siebie, gdy napotyka zagnieżdżone foldery, 
aby program obejmował wszystkie poziomy katalogów.
Skrypt powinien przejść do podanego podczas uruchomienia folderu i posortować wszystkie pliki według rodzajów:

- obrazy ('JPEG', 'PNG', 'JPG', 'SVG');
- pliki wideo ('AVI', 'MP4', 'MOV', 'MKV');
- dokumenty ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
- muzyka ('MP3', 'OGG', 'WAV', 'AMR');
- archiwa ('ZIP', 'GZ', 'TAR');
- nieznane rozszerzenia.
(Możesz powiększyć i uzupełnić tę listę według własnego uznania)

W wynikach pracy powinny się znaleźć:

- Lista plików w każdej kategorii (muzyka, wideo, zdjęcia itp.)
- Wykaz wszystkich znanych rozszerzeń plików, które występują w folderze docelowym.
- Wykaz wszystkich rozszerzeń plików, które pozostały nierozpoznane przez skrypt.
- Następnie należy dodać funkcje odpowiedzialne za przetwarzanie każdego rodzaju plików.

Dodatkowo należy zmienić nazwy wszystkich plików i folderów, 
usuwając wszystkie znaki, które mogą powodować problemy. 
W tym celu do nazw plików możesz zastosować funkcję normalize. 
Pamiętaj jednak, że zmienianie nazw plików nie powinno mieć wpływu na rozszerzenia.

Funkcja normalize:

Zmienia polskie litery na zwyczajne znaki (na przykład, ą, ę, ż itd.)
Zamienia wszystkie litery, oprócz zwyczajnych znaków i cyfr, na znak '_'.

Wymagania dotyczące funkcji normalize:

- przyjmuje ciąg znaków jako argument wejściowy i zwraca ciąg znaków;
- wykonuje transliterację polskich liter zwyczajnymi znakami.
- zamienia wszystkie litery, oprócz zwyczajnych znaków i cyfr, na znak '_'.
- transliteracja może nie być zgodna ze standardem, ale powinna być czytelna;
- pozostaje zachowana wielkość liter (wielkie litery pozostają wielkimi i podobnie w przypadku małych liter) 
po transliteracji.

Instrukcje dotyczące sortowania plików:

obrazy → folder images
dokumenty → folder documents
pliki audio → folder audio
pliki wideo → folder video
zawartość archiwów po rozpakowaniu → folder archives
Kryteria akceptacji pracy domowej

nazwy wszystkich plików i folderów są zmieniane przy użyciu funkcji `normalize`;
- po zmianie nazw plików rozszerzenia pozostają bez zmiany;
- puste foldery są usuwane;
- skrypt ignoruje foldery archives, video, audio, documents, images;
- zawartość rozpakowanego archiwum jest przenoszona 
  do podfolderu o takiej samej nazwie (ale bez rozszerzenia na końcu) w folderze archives;
- pliki o nieznanych rozszerzeniach pozostają bez zmiany.
"""

import os, shutil


def normalize(word):
    normalized = ""

    map = {
        ord("ą"): "a",
        ord("ć"): "c",
        ord("ę"): "e",
        ord("ł"): "l",
        ord("ó"): "o",
        ord("ś"): "s",
        ord("ź"): "z",
        ord("ż"): "z",
        ord("Ą"): "A",
        ord("Ć"): "C",
        ord("Ę"): "E",
        ord("Ł"): "L",
        ord("Ó"): "O",
        ord("Ś"): "S",
        ord("Ź"): "Z",
        ord("Ż"): "Z",
    }
    word = word.translate(map)

    for c in word:
        if 127 < ord(c):
            normalized += "_"
        else:
            normalized += c

    return normalized


def get_files(path):
    lst = list()
    for entry in os.scandir(path):
        if entry.is_dir():
            lst += get_files(path + entry.name + "/")

        if entry.is_file():
            rp = os.path.realpath(path + entry.name)
            lst.append(rp)

    return lst


def delete_empty_folders(root):
    special_folders = ["archives", "audio", "documents", "images", "video"]
    for dirpath, dirnames, _ in os.walk(root, topdown=False):
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if not os.listdir(full_path) and dirname not in special_folders:
                os.rmdir(full_path)


# print("ŚCIEŻKA ABSOLUTNA: " + os.path.abspath(__file__))
# print(" ----------------------------------------------- ")
# print("ŚCIEŻKA PODZIELONA: ", end="")
# print(os.path.split(os.path.abspath(__file__)))
# print(" ----------------------------------------------- ")
# print("ŚCIEŻKA ABSOLUTNA TYLKO FOLDER: " + os.path.split(os.path.abspath(__file__))[0])

path = os.path.dirname(__file__) + "/"
# print("Ścieżka: {}".format(path))
# print(path)
try:
    os.mkdir(path + "images")
    os.mkdir(path + "documents")
    os.mkdir(path + "audio")
    os.mkdir(path + "video")
    os.mkdir(path + "archives")
except:
    pass

all_files = get_files(path)

for file_abs in all_files:
    file = os.path.split(file_abs)[1]

    file = normalize(file)

    if (
        file.endswith(".jpeg")
        or file.endswith(".jpg")
        or file.endswith(".png")
        or file.endswith(".svg")
    ):
        shutil.move(file_abs, path + "images/" + file)
    elif (
        file.endswith(".avi")
        or file.endswith(".mp4")
        or file.endswith(".mov")
        or file.endswith(".mkv")
    ):
        shutil.move(file_abs, path + "video/" + file)
    elif (
        file.endswith(".doc")
        or file.endswith(".docx")
        or file.endswith(".txt")
        or file.endswith(".pdf")
        or file.endswith(".xlsx")
        or file.endswith(".pptx")
    ):
        shutil.move(file_abs, path + "documents/" + file)
    elif (
        file.endswith(".mp3")
        or file.endswith(".ogg")
        or file.endswith(".wav")
        or file.endswith(".amr")
    ):
        shutil.move(file_abs, path + "audio/" + file)
    elif file.endswith(".zip") or file.endswith(".gz") or file.endswith(".tar"):
        shutil.move(file_abs, path + "archives/" + file)

delete_empty_folders(path)
# obrazy ('JPEG', 'PNG', 'JPG', 'SVG');
# pliki wideo ('AVI', 'MP4', 'MOV', 'MKV');
# dokumenty ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
# muzyka ('MP3', 'OGG', 'WAV', 'AMR');
# archiwa ('ZIP', 'GZ', 'TAR');
