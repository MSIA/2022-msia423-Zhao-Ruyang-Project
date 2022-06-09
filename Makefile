.PHONY: clean-data, clean-model clean-all
clean-data:
	rm -f data/download/flight_data.csv
	rm -f data/clean/clean_data.csv
	rm -f data/clean/features.csv
	rm -f data/clean/features.npy
	rm -f data/clean/target.npy
	rm -f data/train/X_train.npy
	rm -f data/train/y_train.npy
	rm -f data/test/X_test.npy
	rm -f data/test/y_test.npy
	rm -f data/predictions/prediction.npy
	rm -f evaluations/report.txt

clean-model:
	rm -f models/encoder.joblib
	rm -f models/model.joblib

clean-all: clean-data clean-model

.PHONY: image-model, image-app, image-test, image-pylint
image-model:
	docker build -f dockerfiles/Dockerfile -t final-project .
image-app:
	docker build -f dockerfiles/Dockerfile.app -t final-project-app .
image-test:
	docker build -f dockerfiles/Dockerfile.test -t final-project-tests .
image-pylint:
	docker build -f dockerfiles/Dockerfile.pylint -t final-project-pylint .

.PHONY: create-db
create-db:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
	-e SQLALCHEMY_DATABASE_URI \
	final-project run_rds.py

.PHONY: model-pipeline
model-pipeline: clean-all get-clean generate-feature train score evaluate

.PHONY: get-clean
get-clean: acquire-data preprocess

.PHONY: persist-s3, acquire-data, preprocess, generate-feature, train, score, evaluate
persist-s3: data/raw/flight_data.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		final-project run_s3.py

data/download/flight_data.csv: run_s3.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		final-project run_s3.py --download
acquire-data: data/download/flight_data.csv

data/clean/clean_data.csv: data/raw/flight_data.csv config/model_config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py preprocess
preprocess: data/clean/clean_data.csv

data/clean/features.npy data/clean/target.npy: data/clean/clean_data.csv config/model_config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py generate_feature
generate-feature: data/clean/features.npy data/clean/target.npy

models/model.joblib: data/clean/features.npy data/clean/target.npy config/model_config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py train
train: models/model.joblib

data/predictions/prediction.npy: models/model.joblib data/test/X_test.npy
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py score
score: data/predictions/prediction.npy

evaluations/report.txt: data/predictions/prediction.npy data/test/y_test.npy
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py evaluate
evaluate: evaluations/report.txt

.PHONY: run-app run-test
run-app:
	 docker run \
	 --mount type=bind,source="$(shell pwd)",target=/app/ \
	 -e SQLALCHEMY_DATABASE_URI \
	 -p 5001:5001 final-project-app

run-test:
	docker run final-project-tests
