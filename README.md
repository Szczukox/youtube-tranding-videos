# youtube-tranding-videos

##### Autorzy
- Adrian Kotarski 127346 
- Patryk Szczuczko 127215

## Etap 1
### Opis działań
Początkowo dane z obydwu plików łączymy w jeden większy zbiór danych, dodając
jednocześnie atrybut rozróżniający skąd dane pochodzą (atrybut 'country').

Następnie dodajemy dwa nowe atrybuty utworzone na podstawie istniejących już atrybutów, 
opisujące długość tytułu i opisu (odpowiednio: 'title_length' oraz 'description_length').
Atrybuty zostaną wykorzystane, by sprawdzić jaki jest rozkład wartości na tych atrybutach
oraz czy istnieje korelacja pomiędzy tymi wartościami a popularnością video. 

Ta sama motywacja była podstawą do utworzenia dwóch innych atrybutów: liczby tagów (atrybut 'number_of_tags')
oraz liczby linków (atrybut 'number_of_links'). 

Jeśli chodzi o atrybuty 'trending_date' oraz 'publish_date' to ich struktura została ujednolicona,
tzn. wszystkie dane zostały sprowadzone do informacji o dacie. Dodatkowo z atrybutu 'publish_time'
zostały utworzone kolejne dwa atrybuty: rok (atrybut 'publish_time_year') oraz miesiąc (atrybut
'publish_time_month') publikacji video. Atrybuty te zostaną wykorzystane do grupowania filmów na podstawie
wartości tych atrybutów i sprawdzeniu czy jest jakaś tendencja odnośnie popularności video w zależności
od miesiąca opublikowania.

Kolejnymi atrybutami, które są rozszerzeniami istniejących są: stosunek liczby like'ów, dislike'ów i komentarzy do liczby wyświetleń. Pozwala to określić jak duża część oglądających angażuje się w filmik, tj. czy dużo osób oglądających pokazuje jakąkolwiek reakcję, czy może jest to duża liczba wyświetleń przypadkowych osób, które "nabijają" tylko tę statystykę. Istniejące atrybuty w postaci surowej liczby wyświetleń/like'ów/dislike'ów/komentarzy też mogą być przydatne przy analizie, być może istnieją pewne progi, po których szansa na bycie filmiku w trending znacząco rośnie.

Został utworzony również atrybut 'days_from_publish_time_to trending_date', którego wartość stanowi
liczbę dni, które upłynęły od czasu opublikowania filmu, do czasu w którym film trafił do zakładki
Trending (czyli jest to po prostu różnica między 'trending_date' a 'publish_time' wyrażona w dniach).
Utworzenie tego atrybutu jest umotywowane tym, że filmy, które nie potrzebują dużo czasu od opublikowania
ich, żeby trafiły do zakładki Trending, być może jakoś bardziej się wyróżniają i należy dokładniej
przeanalizować dane takich video.

Następnym etapem naszych działań była wizualizacja danych na wykresach. Za pomocą wykresów pudełkowych
zobrazowaliśmy rozkład wartości dla atrybutów: 'number_of_tags', 'number_of_links', 'title_length' oraz
'description_length'. Zrobiliśmy to zarówno na całym zbiorze danych, jak i dla podziału na kraje GB i US,
aby sprawdzić czy są w tej kwestii jakieś wyraźne różnice, jeśli chodzi o porównanie video brytyjskich
i amerykańskich. Okazało się, że te różnice nie są znaczące.

Sprawdziliśmy również jakie kategorie dominują w zbiorze danych. Niestety, okazało się, że filmy z przypisaną
kategorią stanowią około 6% wszystkich filmów. Dlatego ciężko byłoby wysnuć jakąś prawidłowość na podstawie
tylko tego atrybutu. Mimo to, na wykresie przedstawiliśmy, które kategorię filmów, są najbardziej popularne
(stwierdziliśmy, że film popularny powinien mieć dużo wyświetleń, like'ów oraz komentarzy).

Jeśli chodzi o popularność filmów w zależności od miesiąca w jakim zostały one opublikowane, to dane pokazują,
że filmy opublikowane od lipca do października nie cieszą się dużą liczbą wyświetleń i polubień. Z drugiej strony,
liczba filmów opublikowana w tym okresie również jest bardzo mała. Biorąc te dwie kwestię pod uwagę, być może
opublikowanie filmu w okresie lipiec-październik, ma większe szanse na trafienie do zakładki Trending, nawet jeśli
nie będzie miało zbyt dużej liczby wyświetleń, polubień czy komentarzy. Chociaż najbardziej prawdopodobny jest tutaj brak zbalansowania przykładów przypadających na dany miesiąc, tj. dataset został głównie zbudowany w oparciu o przykłady z pozostałych miesięcy.

Sprawdziliśmy także, czy fakt wyłączenia możliwości komentowania lub oceny filmu wpływa negatywnie na jego liczbę odsłon.
Według danych ze zbioru taka teza jest nieprawdziwa, jednak liczba filmów z wyłączoną opcją komentowania lub oceniania jest znikoma,
więc mimo tego, że takie ograniczenie nie wpływa na liczbę odsłon to mała ilość takich filmów może sugerować, że nie są
one zbyt chętnie brane do zakładki Trendings.

Ostatnią obserwacją jest przedstawienie macierzy korelacji. Wynika z niej dodatnia korelacja między kilkoma grupami atrybutów.
Pierwszą grupę stanowią atrybuty: 'views', 'likes', 'dislikes' oraz 'comment_count'. Jest to dosyć zrozumiałe, gdyż logicznym
wydaje się, że jeśli film będzie miał więcej odsłon to więcej użytkowników go oceni oraz skomentuje. Drugą grupą skorelowaną są atrybuty:
'comments_disabled' oraz 'ratings_disabled', co oznacza że jeśli komentowanie jest wyłączone to ocenianie również. Z macierzy można też
zaobserwować fakt, że filmy które mają dużo tagów, częściej mają też dużo linków w opisie. Negatywną korelacją wykazują atrybuty 'publish_time_year'
oraz 'days_from_publish_time_to_trending_date', co świadczy o tym, że filmy opublikowane wcześniej czekały dłużej na to, aby
zaistnieć w zakładce Trendings. Jednak może mieć to związek z tym, że dany film pojawił się kilka razy w zakładce Trendings,
a 'trending_date' to data ostatniego razu kiedy ten film się tam pojawił. Jeśli chodzi o grupy skorelowanych atrybutów, to z każdej
takiej grupy do dalszego przetwarzania i uzyskiwania wiedzy będzie wybrany jeden z nich, aby taka grupa nie miała sztucznie zwiększonej wagi ważności.

Zdecydowaliśmy się też nie wykorzystywać zliczania słów w tytułach/opisach, jako że są one bezpośrednią implikacją treści filmiku jak i ogólnej działalności kanału. Nie ma więc sensu analiza i doszukiwanie się wzorców w tych danych, jeśli muszą one wynikać wyłącznie z charakteru filmiku i kanału, które zależą wyłącznie od youtubera. Sztuczna próba tworzenia contentu na podstawie losowych zlepków słów niezwiązanych z działalnością twórcy jest bezcelowa.

### Wnioski
- Liczba tagów jest podobna dla regionów US i GB i oscyluje mniej więcej w granicach 10-30.
- Liczba linków w opisie analogicznie, wynosi mniej więcej 5.
- Długość tytułu: średnio około 50 znaków
- Długość opisu: średnio nieco ponad 600.
- Dominują kategorie "rozrywka" i "muzyka", aczkolwiek jak wcześniej wspomniane filmiki z przypisaną kategorią stanowią niewielki odsetek całego zbioru danych
- W miesiącach czerwiec - październik jest bardzo mało filmów, prawdopodobnie niezbalansowany zbiór danych.
- Wyłączona możliwość oceniania nie ma większego wpływu na wyświetlenia.

Atrybuty, których nie da się wykorzystać lub są nieprzydatne:
- 'video_id' - służy tylko jako ID video i nie da się nic z tego wywnioskować
- 'channel_title' - są to nazwy własne, często nazwiska, i nie ma sensu tego analizować
- liczba wystąpień danych słów w jakichkolwiek łańcuchach znaków - youtube zawiera różnorodne filmiki, a słowa związane z nimi są ściśle powiązane z tematyką, którą obejmują, więc jeśli celem jest dostanie się do zakładki trendings, to zakładamy, że słowa związane z filmikiem będą naturalną implikacją jego treści, a nie losowym zlepkiem najczęściej występujących słów, z zupełnie innej kategorii.

W ogólności ciekawsze wnioski będzie można sformułować w momencie konfrontacji powyższych statystyk ze statystykami ze zbioru filmików niewystępujących na trending. Wówczas być może wyłonią się pewne różnice w filmikach z obu zbiorów danych. Na ten moment rozszerzona analiza nie jest aż tak istotna, gdyż nie wiemy jak ma się to do filmików niewystępujących na trending (analiza danej statystyki okaże się być stratą czasu, jeśli filmiki trending nie będą się nią odróżniały od nie-trending).

### Aktualizacja do Etapu 1
- Po bardziej wnikliwym przejrzeniu zbioru danych okazało się że atrybut 'video_id' nie jest unikalny.
W związku z tym zliczyliśmy liczbę wystąpień dla każdej wartości 'video_id' i utworzyliśmy na jej podstawie
nowy atrybut 'trending_count'. Zdecydowaliśmy się usunąć wpisy z tymi samymi 'video_id' w taki sposób,
że zostawiliśmy wpis z najpóźniejszą datą w atrybucie 'trending_date' jednocześnie zmieniając jej nazwę na
'last_trending_date'. Dzięki tej operacji atrybut 'video_id' stał się unikalny.
Jednocześnie utworzyliśmy atrybut 'first_trending_date', który zawiera datę pierwszego
ukazania się filmu o danym 'video_id' w zakładce Trending.
- W ramach realizacji operacji z poprzedniego punktu został wykryty również fakt, że atrybut 'video_id'
posiadał również błedną wartość '#NAZWA?'. Jako, że w Etapie 2 zajmujemy się tylko atrybutami wizualnymi,
postanowiliśmy póki co usunąć te wpisy ze zbioru danych. Stanowią one około 1% wszystkich wpisów w zbiorze,
więc strata danych nie jest duża. Natomiast po analizie wpisów z tym błędnym 'video_id', wydaje się, że lepszym
pomysłem jest zbudowanie unikalnych 'video_id' z części atrybutu 'thumbnail_link', z których (jak wynika z naszych
obserwacji) są zbudowane również inne, prawidłowe wartości 'video_id'. Ten pomysł zrealizujemy w ramach Etapu 3.

## Etap 2
- Na początku napisaliśmy funkcję odpowiadającą za pobranie wszystkich obrazków i zapisanie ich do katalogu 'thumbnails'.
Okazało się, że nie wszystkie filmiki posiadają swoją miniaturkę.
- Przeglądając pobrane miniaturki zaobserwowaliśmy pewną prawidłowość, że przy górnych i dolnych krawędziach
występują czarne paski. Postanowiliśmy więc uciąć minaturki o 10 pikseli z góry i 10 pikseli z dołu, aby
późniejsze tworzenie atrybutów na podstawie charakterystyki pikseli nie było przekłamane.
- Następnie zostały utworzone atrybuty oparte na charakterystyce pikseli:
    - w przestrzeni RGB - średni kolor piksela (atrybuty: 'average_red', 'average_green', 'average_blue')
    oraz wartość dominująca ('mode_red', 'mode_green', 'mode_blue'),
    - w przestrzeni HSV - średnia wartość piksela (atrybuty: 'average_hue', 'average_saturation', 'average_value')
    oraz wartość dominująca ('mode_hue', 'mode_saturation', 'mode_value'), a także liczba pikseli mieszcząca się
    w danym przedziale wartości hue ('hue_red', 'hue_yellow', 'hue_green', 'hue_cyan', 'hue_blue', 'hue_magenta')
    - w skali szarości - kontrast RMS (root mean square)
- W przypadku wykrywania elementów na miniaturkach zdecydowaliśmy się na użycie gotowych pretrenowanych modeli z biblioteki Keras, tj. VGG16, ResNet, InceptionV3 i MobileNet. W zamyśle miały one posłużyć do wykrycia różnego rodzaju obiektów na miniaturce, tak aby umożliwić przeprowadzenie analizy z nimi związanej. Być może udałoby się w ten sposób wyznaczyć jakieś trendy. Niestety próby pracy z powyższymi modelami nie przyniosły żadnych rezultatów - testy pokazały, że te modele zupełnie nie radzą sobie z miniaturkami, które posiadamy. Wyniki, które zwracają są nietrafione i podawane z bardzo małą pewnością w większości przypadków, prawdopodobnie wynika to z tego, iż na miniaturkach najczęściej pojawiają się ludzie, a modele skupiają się na wykrywaniu zwierząt, elementów otoczenia czy garderoby. Wobec tego zdecydowaliśmy się pominąć w analizie wykorzystanie powyższych rozwiązań.
Prawdopodobna dodatkowa przyczyna słabych wyników to również fakt, że miniaturki są małego rozmiaru, w dodatku część obrazu stanowią czarne poziome paski, co przekłada się na efektywny obraz rozmiaru 120x68. Większość modeli obsługuje rozmiar 224x224 i rozciągnięcie obrazu do tych wymiarów wiąże się z dużymi zniekształceniami obrazu, co daje w efekcie obraz słabej jakości.
- Wykorzystaliśmy za to inny [model](https://github.com/jalajthanaki/Facial_emotion_recognition_using_Keras). Podane rozwiązanie wymagało odpowiedniej modyfikacji, gdyż oryginalnie program analizował pojedynczy plik i wyświetał obraz z naniesionymi zaznaczeniami twarzy wraz z rodzajem emocji. Kod został zmieniony tak, aby dla każdej z naszych miniaturek (już bez duplikatów) zwrócił odpowiadający wektor z liczbami wystąpień poszczególnych rodzajów emocji (jedna miniaturka może pokazywać np. dwie smutne osoby i jedną wesołą). Wyniki zostały zapisane do oddzielnego pliku .csv, aby uniknąć częstego wykonywania długotrwałych obliczeń. Ostatecznie w głównym skrypcie tworzony jest nowy atrybut z wektorem liczby wystąpień emocji na podstawie tego pliku.
### Wnioski
- Przeważający przedział kolorów, który występował na miniaturkach to czerwony. Było go około 2-krotnie więcej od przedziałów żółtego i niebieskiego, zajmujących w przybliżeniu na równi drugie miejsce co do częstości występowania. Oznacza to, że być może warto przemyśleć wykorzystanie wymienionego przedziału koloru, być może przeciętny widz reaguje na czerwone odcienie nieco pozytywniej od innych kolorów. Nie można jednak wykluczyć, że dominacja czerwonego jest po prostu spowodowana występowaniem twarzy na dużej części miniaturki. Kolory skóry prawdopodobnie najczęściej posiadają taką właśnie barwę, o ile nie są oświetlone specyficznym światłem. Należałoby tutaj przeprowadzić głębszą analizę.
- Najczęściej występującymi emocjami na miniaturkach były smutek, radość oraz neutralność. Dwukrotnie rzadziej występowały gniew i strach, zaskoczenie około 5-krotnie rzadziej. Wynikałoby z tego, że widzowie najsilniej reagują na widok 3 wcześniej wymienionych emocji i miniaturki powinny je zawierać. Należy mieć jednak na względzie, że zastosowano heurystyczny model, który wiąże się z nieuniknionymi pomyłkami. Należy traktować te wyniki z pewną dozą ostrożności.
Analiza może jeszcze zostać rozszerzona w kolejnych etapach w miarę zdobywania nowych obserwacji.

## Etap3
Na początku poprawiliśmy kilka kwestii, których nie zrobiliśy w poprzednim etapie:
- Zmieniliśmy kwestię redukcji rekordów: dla wpisów z tym samym 'video_id' zostawiamy rekord z datą pierwszego
pojawienia się w Trendings. Wcześniej był to rekord z datą ostatniego pojawienia się w zakładce Trendings
- Tak jak wspomnieliśmy w ramach aktualizacji do etapu 1, błędne 'video_id' (z wartością '#NAZWA?') można
zastąpić ID wygenerowanym z wartości atrybutu 'thumbnail_link', w którym jest obecny prawidłowy 'video_id'
(przykład: ht<span>tps://</span>i.ytimg.com/vi/Jw1Y-zhQURU/default.jpg -> Jw1Y-zhQURU). W tym etapie udało się
zastosować tę operację, co pozwoliło na uzyskanie dodatkowych kilkuset rekordów. Wcześniej po prostu usuwaliśmy
rekordy z 'video_id' == '#NAZWA?'.

### Analiza atrybut�w i ich zale�no�ci
- wy�wietlenia, lajki, komentarze - du�a korelacja, mo�liwa redukcja
- kolory
- itd.
### Wybrane atrybuty
- atrybut1
- atrybut2
- itd.
### Analiza atrybut�w pod k�tem przydatno�ci przy etykietowaniu i ostatecznej wiedzy
- na viewy itp. nie mamy wp�ywu, ale mog� si� przyda� do predykcji momentu wej�cia na trending
- itd.
