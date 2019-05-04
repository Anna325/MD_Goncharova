# Конвертация корпуса во внутренне представление
1. Подготовка папок для корпусов:
```
mkdir data
mkdir data/OpenCorpora
mkdir data/UD
mkdir data/NKRY
mkdir data/GIKRY
```

###### OpenCorpora
Корпус в разметке OpenCorpora надо разместить в папке `data/OpenCorpora`, а файл назвать `annot.opcorpora.xml`.
###### UD
Корпус в разметке UD надо разместить в папке `data/UD`, а файл назвать `text.txt`.
###### NKRY
Все файлы корпуса (файлы с текстами) разместить в папке `data/NKRY`
###### GIKRY
Все файлы корпуса (файлы с текстами) разместить в папке `data/GIKRY`

2. Подготовка папок для временных файлов:
```
mkdir tmp
mkdir tmp/gikry
mkdir tmp/ud
mkdir tmp/nkry
mkdir tmp/nkry/texts
mkdir tmp/oc
```
3. Запуск конвертации во внутреннее представление:
```
python main.py prepare ud
python main.py prepare oc
python main.py prepare nkry
python main.py prepare gikry
```

# Обучение моделей
1. Подготовка папок для файлов моделей:
```
mkdir model
mkdir model/gikry
mkdir model/ud
mkdir model/nkry
mkdir model/oc
mkdir model/oc/classifier
```

2. Обучение CRF-моделей
```
python main.py train nkry
python main.py train gikry
python main.py train oc
python main.py train ud
```

3. Обучение нейронной сети
```
python main.py train_classifier oc pos
python main.py train_classifier oc case
python main.py train_classifier oc trans
python main.py train_classifier oc invl
python main.py train_classifier oc verbForm
python main.py train_classifier oc degree
```

# Тестирование точности с выводом ошибок
```
python main.py reconvert ud
python main.py reconvert oc
python main.py reconvert nkry
python main.py reconvert gikry
```

# Точность преобразований
|Конвертация|Точность без моделей|Точность с  CRF|Точность с RNN|
|-|-|-|-|
|OpenCorpora -> UD -> OpenCorpora|79.84%|94.54%|89.05%|
|UD -> OpenCorpora -> UD|88.8%|97.79%||
|GIKRY -> UD -> GIKRY|73.81%|94.20%||
|NKRY -> UD -> NKRY|81.75%|93.70%||




