FROM public.ecr.aws/lambda/python:3.12

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Копируем код
COPY main.py config.py ${LAMBDA_TASK_ROOT}

# Указываем точку входа: файл.функция
CMD ["main.handler"]