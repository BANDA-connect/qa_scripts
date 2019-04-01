import pandas as pd
import tensorflow as tf

train_path="/space/erebus/1/users/data/preprocess/anatomicuts_values_train.csv"
test_path="/space/erebus/1/users/data/preprocess/anatomicuts_values_test.csv"

#CSV_COLUMN_NAMES = ['FA', 'MD', 'RD', 'AD', 'Anhedonia']
CSV_COLUMN_NAMES= ['FA11101101', 'FA1110110000', 'FA1110110001', 'FA1110110010', 'FA1110110011', 'FA111111000', 'FA111111001', 'FA111111010', 'FA111111011', 'MD11101101', 'MD1110110000', 'MD1110110001', 'MD1110110010', 'MD1110110011', 'MD111111000', 'MD111111001', 'MD111111010', 'MD111111011', 'RD11101101', 'RD1110110000', 'RD1110110001', 'RD1110110010', 'RD1110110011', 'RD111111000', 'RD111111001', 'RD111111010', 'RD111111011', 'AD11101101', 'AD1110110000', 'AD1110110001', 'AD1110110010', 'AD1110110011', 'AD111111000', 'AD111111001', 'AD111111010', 'AD111111011', 'Anhedonia']
SPECIES = [0,1]
CSV_TYPES = [] #[0.0], [0.0], [0.0], [0.0], [0]]
for a in range(len(CSV_COLUMN_NAMES)-1):
	CSV_TYPES.append([0.0])
CSV_TYPES.append([0])

def load_data(y_name='Anhedonia'):
    """Returns the iris dataset as (train_x, train_y), (test_x, test_y)."""

    train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
    train_x, train_y = train, train.pop(y_name)

    test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)
    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)


def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(10000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset


# The remainder of this file contains a simple example of a csv parser,
#     implemented using the `Dataset` class.

# `tf.parse_csv` sets the types of the outputs to match the examples given in
#     the `record_defaults` argument.
def _parse_line(line):
    # Decode the line into its fields
    fields = tf.decode_csv(line, record_defaults=CSV_TYPES)

    # Pack the result into a dictionary
    features = dict(zip(CSV_COLUMN_NAMES, fields))

    # Separate the label from the features
    label = features.pop('Anhedonia')

    return features, label


def csv_input_fn(csv_path, batch_size):
    # Create a dataset containing the text lines.
    dataset = tf.data.TextLineDataset(csv_path).skip(1)

    # Parse each line.
    dataset = dataset.map(_parse_line)

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(10000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset
