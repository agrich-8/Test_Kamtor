# Test_Kamtor

1.

Каждую минуту сохраняем значение, берем производную изменения цены - находим скорость изменения ( для обоих коинов). При изменении менее 0.1% - свеча дожи, в расчетах не учитываем, пропускаем.

Если производные имеют разные знаки, делаем вывод, что цена ETH обусловлена естественным наполнением стакана, не связана с движением цен на биткоин - значит движение собственное .

Так же будет правильно учитывать коэффициент изменения, но для этого нужен глубокий анализ рынка, поэтому введу свое условие: если отношение свеч ETH к BTC равно 3 при одинаковом знаке, то движение читается собственным


2.

Если правильно понял, программа должна выводить цену ETH при изменении на 1% именно при собственном движении. Для более точного определения необходим глубокий анализ, я приму движение за собственное при условии: 70% времени в течение часа ETH имел собственное движение ( то есть 42 минуты из 60 движения изменения цен имели разные знаки или отношение по модулю равное 3)
