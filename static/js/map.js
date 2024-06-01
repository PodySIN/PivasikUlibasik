ymaps.ready(init);
    var myMap;
    var placemarks = [];

    function init() {
        myMap = new ymaps.Map("map", {
            center: [60.05602766434451,30.424292527895506],
            zoom: 15
        });

        var coords = [
            [60.055847085725105,30.421652289291405],
            [60.05866803332129,30.42317159057505],
            [60.05840313168452,30.424864531890506],
            [60.05592859354674,30.426952126965247],
            [60.069319512986496,30.425693731981386],
            [60.057505569607294,30.420691675256034],
            [60.05337408502316,30.414426471021816]
        ];

        var address = [
            'Воронцовский',
            'Петровский',
            'Шувалова',
            'Купчинский',
            'Будапештский',
            'Берлинский',
            'Заморский'
        ];

        for (var i = 0; i < coords.length; i++) {
            var placemark = new ymaps.Placemark(coords[i], {
                hintContent: 'Метка ' + (i + 1),
                balloonContent: address[i]
            });

            placemarks.push(placemark);
            myMap.geoObjects.add(placemark);
        }
    }

    function goToPlacemark(index) {
        if (index-1 < placemarks.length) {
            myMap.setCenter(placemarks[index-1].geometry.getCoordinates(), 18);
            placemarks[index-1].balloon.open();
        } else {
            alert('Нет такой метки');
        }
}