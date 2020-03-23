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
nie będzie miało zbyt dużej liczby wyświetleń, polubień czy komentarzy.

### Wnioski
Atrybuty, których nie da się wykorzystać:
- 'video_id' - służy tylko jako ID video i nie da się nic z tego wywnioskować