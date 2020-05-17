import click
from . import model
from .io import input, set_data_frame, output, test
from datetime import datetime


@click.command()
@click.option('--train/--no-train', default=False, help="Train the model.")
@click.option('--predict/--no-prediction', default=False, help="do something!")
@click.option('--transform/--no-prediction', default=False, help="do something!")
@click.argument('csv_file', type=click.File("rb"))
@click.option('--testing_code/--no_testing', default=False, help="Can be used for prototyping")
def main(train, transform, csv_file, predict, testing_code):
    if train:
        model.train()
    else:
        print("You don't do anything.")

    if transform:
        # read file return data frame object
        df = input.read_file(csv_file)

        # created new format df and return it
        df_tran = set_data_frame.create_df(df)

        # write result df to csv file
        output.write_file("transform_DF", df_tran)

    if predict:
        print("Hallo")

    if testing_code:
        print("Testing class used")
        test.testing_code(csv_file)

if __name__ == '__main__':
    main()

