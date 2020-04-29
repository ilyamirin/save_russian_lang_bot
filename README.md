
## 1) Установка docker
https://docs.docker.com/engine/install/ubuntu/
## 2) Добавление текста для отправки
```
mkdir data
cd data
mkdir text_files
```
И добавить туда файлы .txt
## 3) Запуск бота:
Для gnu/linux есть bash-скрипт deploy.sh,
вручную:
```

mkdir voice
cd ..
docker build путь-до-папки-проекта -t savior
docker run --name saviord -d -v путь-до-папки-проекта/data:/data:rw savior
```
## (Дополнительно) конфигурация скрипта savior.py
по аргументу -t / --text может принимать список файлов txt для добавления. По умолчанию принимает все.