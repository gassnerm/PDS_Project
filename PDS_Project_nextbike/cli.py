import click
from .import model
from .model import create_predictors
from .io import input, set_data_frame, output, save_model, read_file
from datetime import datetime
from .model import train_nn_classification_task, create_predictors, prediction


@click.command()
@click.option('--train/--no-train', default=False, help="Train the model. Use the frankfurt_all.csv file train the model. "
                                                        "It will split the test and the training set  ")
@click.option('--predict/--no-prediction', default=False, help="Select hier a filepath relativ to the data folder "
                                                               "of the project to predict a certain file.")
@click.option('--transform/--no-prediction', default=False, help="Tipe in a foldername you want to select for transformation of the file. "
                                                                 "It will be stored under the name you selected in the target file parameter relativly "
                                                                 "to the output data folder."
                                                                 "Use --transform <sourcefile_name>  <target_file>")
@click.argument('csv_file', type=str, default=False)
@click.argument('target_file', type=str, default=False)
@click.option('--testing_code/--no_testing', default=False, help="Can be used for prototyping")
def main(train, transform, csv_file, predict, testing_code, target_file):

    # create intial df of trip format
    if transform:
        # read file return data frame object
        df = read_file(csv_file)

        # created new format df and return it
        df_tran = set_data_frame.create_df(df)

        # if target_file is defined in the command line stored the
        # data in selected path in reference to data folder
        # in that path else it safes the file under data/transform_DF file
        if target_file == False:
            # write result df to csv file
            output.write_file("transform_DF", df_tran)
        else:
            output.write_file(target_file, df_tran)


    # predict model
    if predict:

        # read file return data frame object
        df = read_file(csv_file)

        # created new format df and return it
        # load test data to create features
        df_tran = set_data_frame.create_df(df)
        df_test = set_data_frame.create_df(read_file("frankfurt.csv"))
        df_tran = df_tran.append(df_test)
        df_tran.reset_index(inplace=True, drop=True)
        print("predict:", len(df_tran))

        # create test set predictors for classification flag to set the if the training will
        # be dropped test set data from past required to predict
        # create prediction for test set for classification
        print("predict classification task")
        X_clas, Y_clas = create_predictors.create_predictors_classification(df_tran, False)
        prediction.create_classification_prediction(X_clas, Y_clas)

        print("predict classificattion ends hier")


        # create test set predictors duration and create prediction for test set durations
        print("predictor for  trip duration created  Starts hier")
        X_dura, Y_dura, scaler = create_predictors.create_prediction_Duration(df_tran, False)
        prediction.create_duration_prediction(X_dura, Y_dura, scaler)
        print("predictor for trip duration ends hier")

    # train the models
    if train:

        print("Training starts: ")
        df = read_file(csv_file)

        # create data frame
        csv_file = set_data_frame.create_df(df)

        print("Load test set to create feature preditore for past values ")
        # append test data to create features
        df_test = set_data_frame.create_df(read_file("frankfurt_test.csv"))
        csv_file = csv_file.append(df_test)


        print("Train nn for classification")
        # create the predictors for classification and set train flag to
        # true to drop the test set after feature creation see above
        X_clas, Y_Class = create_predictors.create_predictors_classification(csv_file, True)

        print(type(Y_Class), type(X_clas))

        print("Predictor sucessful created.")
        # train the model for trip direction and save it
        model.train_nn_classification_task(X_clas, Y_Class)
        print("Train for nn ends sucessfull")


        # create predictors for trip duration
        x_duration, y_duration, scaler = create_predictors.create_prediction_Duration(csv_file, True)

        # train the model for duration and save it
        model.train_prediction_duration(x_duration, y_duration, scaler)

if __name__ == '__main__':
    main()
