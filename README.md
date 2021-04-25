# Chat Statistic Bot
Бот для отслеживания статистики в различных чатах. 

![start](https://i.imgur.com/0Z4EoSz.png)
![cmds](https://i.imgur.com/EVHoNDs.png)

### Основное

Команды бота:

```shell

/start (in private, all)
/help (in private, all) - помощь
/list (in private, all) - список чатов для просмотра статистики
/stats ?:([chat_id] [user_id]) (in private, admins) - просмотр личной статистики или статистики пользователя
/addowner [chat_id] [user_id] (in private, only owner) - добавить пользователя в список админов для отслеживания статистики
/removeowner [chat_id] [user_id] (in private, only owner) - убрать пользователя из списка админов для отслеживания статистики чатов
[reply] /id (in supergroup, admins) - узнать ID человека по пересылу
/bind (in supergroup, only owner) - привязать чат к себе
/unbind (in supergroup, admins) - отвязать чат от себя
```

Возможности:

 - Подключение/отключение чата создателю к себе

![bind](https://i.imgur.com/RnKnyvM.png)

 - Подключение/отключение чата к другому пользователю создателем

![addowner](https://i.imgur.com/tJtV6x7.png)
![removeowner](https://i.imgur.com/yHfJS7P.png)

 - Смотреть ID пользователей

![id](https://i.imgur.com/XxArX8u.png)

 - Система уровней и опыта для отельных участников чата и самого чата, а также личная статистика, разрастающаяся в геометрической прогрессии

![lstats](https://i.imgur.com/lWowoKx.png)
![cstats](https://i.imgur.com/MblKBlt.png)

 - Система просмотра до топ 5 пользователей беседы
 
![top](https://i.imgur.com/taG8rxU.png)

 - Система просмотра статистики отдельного пользователя

![stats](https://i.imgur.com/sWRSIeK.png)
