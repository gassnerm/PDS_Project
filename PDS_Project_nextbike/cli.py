import click
from . import model
from .model import create_predictors
from .io import input, set_data_frame, output, test
from datetime import datetime
from .model import train_nn_classification_task, create_prediction_Duration


@click.command()
@click.option('--train/--no-train', default=False, help="Train the model.")
@click.option('--predict/--no-prediction', default=False, help="do something!")
@click.option('--transform/--no-prediction', default=False, help="do something!")
@click.argument('csv_file', type=click.File("rb"), default=False)
@click.option('--testing_code/--no_testing', default=False, help="Can be used for prototyping")
def main(train, transform, csv_file, predict, testing_code):

    if transform:
        # read file return data frame object
        df = input.read_file(csv_file)

        # created new format df and return it
        df_tran = set_data_frame.create_df(df)

        # write result df to csv file
        output.write_file("transform_DF", df_tran)

    if predict:
        print("Hallo")

    if train:
        train_nn_classification_task(csv_file)
        create_prediction_Duration(csv_file)

if __name__ == '__main__':
    main()
