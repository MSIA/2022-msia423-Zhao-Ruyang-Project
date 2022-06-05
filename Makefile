.PHONY: clean-data, clean-model clean-all
clean-data:
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

.PHONY: image-model, image-app
image-app:
	docker build -f dockerfiles/Dockerfile.app -t final-project-app .
image-model:
	docker build -f dockerfiles/Dockerfile -t final-project .

.PHONY: model-pipeline, acquire-data, preprocess, generate-feature, train, score, evaluate

data/raw/flight_data.csv: run_s3.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		final-project run_s3.py --download
acquire-data: data/raw/flight_data.csv

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

model-pipeline: clean-all image-model acquire-data preprocess generate-feature train score evaluate

.PHONY: run-app
run-app:
	 docker run \
	 --mount type=bind,source="$(shell pwd)",target=/app/ \
	 -e SQLALCHEMY_DATABASE_URI \
	 -p 5001:5001 final-project-app

.PHONY: create-db
create-db:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
	-e SQLALCHEMY_DATABASE_URI \
	final-project run_rds.py