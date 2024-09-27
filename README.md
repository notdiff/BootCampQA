<p align="center">
    <img alt="logo" src="https://acdn.tinkoff.ru/static/pages/files/6d109418-912e-4ae4-9f55-34cdce5ee273.png" width='35%'>
</p>

<h2 align="center">
    QA Система
</h2>

Чекпоинт обученной модели доступен [здесь](https://drive.google.com/file/d/1q1Yai2zuvAomZalVKamDO15se1Aur8ir/view?usp=sharing)<br>
Для тестирование модель доступна в [telegram](https://t.me/qamodel_bot)

#### Содержание репозитория
* [./bot/](https://github.com/notdiff/BootCampQA/tree/main/bot) - Код инференса модели в телеграмм боте
* [ideas.ipynb](https://github.com/notdiff/BootCampQA/blob/main/notebooks/ideas.ipynb) - Ноутбук в котором собранны протестированные идеи

## Подробнее о решении
* Решение прадставляет собой модель поиска start-end токенов ответа в вопросе. В качестве основы была взята модель distillBert из-за ее легковесности, она была дообучена на датасете [sberquad](https://huggingface.co/datasets/kuznetsoffandrey/sberquad).<br>
* Метрика (F1Score):
  - Слова предсказанного ответа и целевого лематизировались, убирались все не буквенные символы
  - Итоговая метрика равна 
