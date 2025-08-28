<h1 align="center">Phasalo Bot Template</h1>
<p align="center">
Полпути к идеальному боту. Красиво, как всегда.
</p>
<p align="center">
<img src="https://img.shields.io/badge/made%20by-CSSSensei,%20MaxMavr-439900">
<a href="https://github.com/Phasalo"><img src="https://img.shields.io/badge/Phasalopedia-84D300"></a>
<img src="https://img.shields.io/badge/version-if%20n%20==%202-D1F24E">
</p>

Так много лет нас просили показать, как же мы пишем таких охуительных ботов.
Встречайте — все наши знания в одном репозитории!

Это не просто шаблон, а выжимка сотен часов продакшена, боли и любви к красивому коду.

<h1></h1>

Две пошаговые инструкции для <small>самых маленьких</small>.

## <img src="https://img.shields.io/badge/Рекомендуется-555555"><br> Работа через форк

### 1. Создайте форк репозитория
Нажмите кнопку [`Fork`](https://github.com/Phasalo/PhasaloBotTemplate/fork) в правом верхнем углу и выберите свой аккаунт.

### 2. Клонируйте свой форк
```bash
git clone https://github.com/ВАШ_АККАУНТ/PhasaloBotTemplate.git my-project
cd my-project
```
> Замените `my-project` на имя директории, куда хотите всё сохранить.

### 3. Настройте связь с оригиналом
Чтобы получать обновления
```bash
git remote add upstream https://github.com/Phasalo/PhasaloBotTemplate.git
```

### 4. Проверьте репозитории
```bash
git remote -v
```
Должно показать
```
origin    # ваш форк (чтение/запись)
upstream  # оригинал (только чтение)
```

### Как обновляться из оригинала
Если хотите получить свежие изменения
```bash
git fetch upstream
git merge upstream/main
```
или для перезаписи всех изменений
```bash
git reset --hard upstream/main
```

### Пользуйтесь!
Теперь вы можете:
- Свободно менять код в своём форке
- Создавать новые ветки
- Предлагать изменения в оригинал через Pull Request

## Независимый проект

### 1. Клонируем репозиторий
```bash
git clone https://github.com/Phasalo/PhasaloBotTemplate.git my-project
cd my-project
```
> Замените `my-project` на имя директории, куда хотите всё сохранить.

### 2. Удаляем привязку к оригиналу
```bash
git remote remove origin
```

### 3. Проверяем
```bash
git remote -v
```
> Должно быть пусто — значит, всё получилось.

### Пользуйтесь!

<p align="center">
  <img width="1872" height="888" alt="Phasalo" src="https://github.com/user-attachments/assets/1e33d343-33cb-4682-a172-c654fbcd24a7" />
</p>

<p align="center">
<b>Phasalo</b><br>
<i>Делаем красиво!</i><br><br>
2025
</p>
