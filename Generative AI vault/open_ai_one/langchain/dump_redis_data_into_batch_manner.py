import redis
from itertools import zip_longest

r = redis.Redis(host='localhost', port=6379, db=0)

def batcher(iterable, n):
    """
    Splits an iterable into batches of a specified size.

    Args:
        iterable (iterable): An iterable (e.g., list, iterator) to be batched.
        n (int): The batch size, i.e., the number of items per batch.

    Returns:
        iterator: An iterator that yields tuples of length `n`, with each tuple containing up to `n` items from the iterable.

    Examples:
        >>> list(batcher(range(6), 2))
        [(0, 1), (2, 3), (4, 5)]

        >>> list(batcher(range(6), 3))
        [(0, 1, 2), (3, 4, 5)]

        >>> list(batcher(range(4), 5))
        [(0, 1, 2, 3, None)]
    """
    args = [iter(iterable)] * n
    return zip_longest(*args)


def retrieve_and_process_values(pattern, batch_size):
    """
    Retrieves and processes Redis keys matching a given pattern in batches.

    Args:
        pattern (str): The pattern to match Redis keys (e.g., 'user:*').
        batch_size (int): The number of keys to process in each batch.

    Example:
        If there are 6 list keys in Redis matching 'user:*' (e.g., 'user:0', 'user:1', ..., 'user:5'), and each list key contains values, the function will:
        
        - Process keys in batches of size 2.
        - Retrieve and print values for each key.

    Usage Example:
        >>> r = redis.Redis()
        >>> # Suppose Redis contains the following keys:
        >>> # user:0 -> ['value_0_1', 'value_0_2']
        >>> # user:1 -> ['value_1_1', 'value_1_2']
        >>> # user:2 -> ['value_2_1', 'value_2_2']
        >>> # user:3 -> ['value_3_1', 'value_3_2']
        >>> # user:4 -> ['value_4_1', 'value_4_2']
        >>> # user:5 -> ['value_5_1', 'value_5_2']
        >>>
        >>> retrieve_and_process_values('user:*', 2)
        Processing batch:
        Key: user:0
          Value: value_0_1
          Value: value_0_2
        Key: user:1
          Value: value_1_1
          Value: value_1_2
        Processing batch:
        Key: user:2
          Value: value_2_1
          Value: value_2_2
        Key: user:3
          Value: value_3_1
          Value: value_3_2
        Processing batch:
        Key: user:4
          Value: value_4_1
          Value: value_4_2
        Key: user:5
          Value: value_5_1
          Value: value_5_2

    Notes:
        - The function assumes that the Redis keys are of type 'list'. Modify the function if you need to handle other types.
        - Adjust the `pattern` and `batch_size` as needed based on your specific use case.
    """
    for keybatch in batcher(r.scan_iter(match=pattern), batch_size):
        print("Processing batch:")
        for key in keybatch:
            if key is not None:
                key_type = r.type(key)
                if key_type == 'list':
                    values = r.lrange(key, 0, -1)
                    print(f'Key: {key.decode("utf-8")}')
                    for value in values:
                        print(f'  Value: {value.decode("utf-8")}')
                # Add other key type handling if necessary (e.g., 'string', 'hash', etc.)

