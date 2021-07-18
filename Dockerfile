FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV env=dev
CMD python -m pytest -s --test_results/ /tests_project/tests/