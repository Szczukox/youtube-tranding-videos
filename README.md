# youtube-tranding-videos
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