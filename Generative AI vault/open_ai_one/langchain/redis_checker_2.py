import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Function to create a key with a timestamp in its name
def create_key_with_timestamp(prefix, key, value):
    timestamp = int(time.time())  # Current time as Unix timestamp
    full_key = f"{prefix}:{timestamp}:{key}"  # Format the key with timestamp
    r.set(full_key, value)  # Store the key with its value

# Function to get keys older than a specified age
def get_keys_older_than(prefix, age_seconds):
    current_time = int(time.time())  # Current time as Unix timestamp
    one_hour_ago = current_time - age_seconds  # Calculate threshold time

    # Get all keys with the given prefix
    keys = r.keys(f"{prefix}:*")

    # List to hold keys that are older than the specified age
    old_keys = []

    for key in keys:
        key_str = key.decode('utf-8')  # Decode bytes to string
        
        # Split the key to extract the timestamp
        parts = key_str.split(':')
        if len(parts) >= 2:
            timestamp_str = parts[1]
            try:
                timestamp = int(timestamp_str)
                # Check if the key is older than the specified age
                if timestamp < one_hour_ago:
                    old_keys.append(key_str)
            except ValueError:
                continue  # Ignore keys with invalid timestamp format

    return old_keys

# Example usage
if __name__ == "__main__":
    # Create some example keys with timestamps
    create_key_with_timestamp('demo_test', 'example_key1', 'example_value1')
    create_key_with_timestamp('demo_test', 'example_key2', 'example_value2')

    # Wait a bit to ensure some keys are older
    time.sleep(2)

    # Create another example key with a new timestamp
    create_key_with_timestamp('demo_test', 'example_key3', 'example_value3')

    # Get keys older than one hour (3600 seconds)
    old_keys = get_keys_older_than('demo_test', 3600)
    print("Keys older than one hour:", old_keys)
