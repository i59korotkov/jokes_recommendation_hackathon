# ------------------------------------ #
#   Здесь заданны параметры сервера    #
# ------------------------------------ #

# Путь до папки с данными
UPLOAD_FOLDER = 'jokes_recommendation/data/'

# Путь до папки с логами
LOG_FOLDER = 'jokes_recommendation/log/'

# Путь до папки с моделями
MODELS_FOLDER = 'jokes_recommendation/models/'

# Файлы которые допустимы к загрузке
ALLOWED_EXTENSIONS = {'csv'}

# Шаблон ответа сервера
ANSWER = {
    "Успех": False,
    "Задача": "",
    "Сообщение": ""
}