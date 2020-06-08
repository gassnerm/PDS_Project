import click
from .import model
from .model import create_predictors
from .io import input, set_data_frame, output, save_model, read_file
from datetime import datetime
from .model import train_nn_classification_task, create_predictors, prediction


@click.command()
@click.option('--train/--no-train', default=False, help="Train the model.")
@click.option('--predict/--no-prediction', default=False, help="do something!")
@click.option('--transform/--no-prediction', default=False, help="do something!")
@click.argument('csv_file', type=str, default=False)
@click.option('--testing_code/--no_testing', default=False, help="Can be used for prototyping")
def main(train, transform, csv_file, predict, testing_code):

    # create intial df of trip format
    if transform:
        # read file return data frame object
        df = read_file(csv_file)

        # created new format df and return it
        df_tran = set_data_frame.create_df(df)

        # write result df to csv file
        output.write_file("transform_DF", df_tran)

    # predict model
    if predict:
        # read file return data frame object
        df = read_file(csv_file)

        # created new format df and return it
        df_tran = set_data_frame.create_df(df)

        # create test set predictors for classification
        X_clas, Y_clas = create_predictors.create_predictors_classification(df_tran)

        # create prediction for test set for classification
        prediction.create_classification_prediction(X_clas, Y_clas)

        # create test set predictors duration with degree of 3
        X_dura, Y_dura = create_predictors.create_prediction_Duration(df_tran)

        # create prediction for test set durations
        prediction.create_duration_prediction(X_dura, Y_dura)


    # train the models
    if train:

        df = read_file(csv_file)

        # create data frame
        csv_file = set_data_frame.create_df(df)

        # create the predictors for classification
        X_clas, Y_Class = create_predictors.create_predictors_classification(csv_file)

        # train the model for trip direction and save it
        x_test, y_test = model.train_nn_classification_task(X_clas, Y_Class)

        # create predictors for trip duration
        x_duration, y_duration = create_predictors.create_prediction_Duration(csv_file)

        # train the model for duration and save it
        model.train_prediction_duration(x_duration, y_duration)

if __name__ == '__main__':
    main()
