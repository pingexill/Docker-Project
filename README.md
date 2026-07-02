26. Каталог игр
Название игры, жанр, платформа, рейтинг, описание, год выхода.
Пример таблицы: games: id, title, genre, platform, rating, description, year.
Минимальный функционал: добавление записи, вывод списка, поиск или фильтр, удаление, страница статистики, запуск через Docker с Volume.


Структура: \
    + base(navbar для коорданиций по сайту и подкл style.css. Остальные будут продолжать base..) \
    - welcome_page(Базовая информация, много воды.) \
    - game_list(Список игр в виде table: """ \
        <tr> 
            <th>Название</th> \
            <th>Жанр</th> \
            <th>Платформа</th> \
            <th>Рейтинг</th> \
        </tr> 
        {% for game in games %} 
            <div> 
                <tr> 
                    <td>{{ game[0] }}</td> \
                    <td>{{ game[1] }}</td> \
                    <td>{{ game[2] }}</td> \
                    <td>{{ game[3] }}</td> \
                </tr> 
            </div> 
        {% endfor %} 
        """, сверху search. Сам элемент в списке будет интерактивным - если нажать перейдешь на страницу game/<int:game_id>.) \
    - game/<int:game_id>(Описание, более подробная информация, и т.д. Кнопка удаления этой игрф из списка.) \
    - add_game(Добавление игры в список в виде формы.) \
    - recommend_game(Вывод рандомной игры после нажатия на кнопку. Нажатия на этот элемент будет также редиректать на game/<int:game_id>) \
    - (0207)День 2. (Забыл про статистику) statistics(Сколько игр в датабазе, средний рейтинг, минимальный рейтинг(на него можно будет нажать - redirect(/game/<id [минимальный рейтинг]>)), высший рейтинг(тоже можно нажать), самай старая игра(нажать), самая новая игра(нажать) ) \

Надо добавить(ДБ): +[Завтра после работы с Delete] //0207 \
    - image \
    - creator \
    - price \


=========================================================================

010726: \
    - Работа с структурой ( \
        |-->data \
        |    |--style.css \
        | \
        |-->templates \
        |    |--base.html \
        |    |--welcome_page.html \
        |    |--game_list.html \
        |    |--game.html \
        |    |--add_game.html \
        |    |--recommend_game.html \
        | \
        |--Dockerfile \
        |--main.py \
        |--requirements \
    ) \
    - Заполнение requirements \
    - Заполнение Dockerfile \
    - Добавление @app.root(в сумме 5) \
    - Добавление ф/ций (get_connection, create_table) \
    - Заполнение main.py +/- \
    - Добавление navbar (base.html) 

020726: \
    -main.py( \
        +def add_game() \
        +def game_list() \
        +def game_detail() \
    ) \
    -Добавил всем templates {% extends "base.html" %} \
    -templates( \
        +add_game.html \
        +game_list.html \
        +game.html \
        =base.html(Поменял GameCatalog на Welcome; {% block content %}{%endblock %}) \
    ) 

070726: 
 
080726: 