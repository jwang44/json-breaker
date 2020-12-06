import ijson.backends.yajl2_c as ijson
import json
import os

LARGE_JSON = "/xxx/xx/xxxx/superbig.json" # path to the large json file
TARGET_PATH = "./json"        # directory to put generated smaller json file
RESULT_BATCH_SIZE = 7  # how many items in a resulting smaller json file

# to count how many items are in the iterator
# to do this, it has to iterate till the end
def count_iterator(i):
    return sum(1 for e in i)

file = open(LARGE_JSON, "rb")
items = ijson.items(file, "item")
number_of_items = count_iterator(items)
print("total items: ", number_of_items)
file.close()


# in order to use the elements in the iterator, 
# we have to open it again
file = open(LARGE_JSON, "rb")
items = ijson.items(file, "item")

item_list = []
for x in range(number_of_items+1): 
    # +1 in order to push to the limit and raise StopIteration
    try:
        item = next(items) # item is a dict
        item_list.append(item)
        print(x)
        if (x+1)%RESULT_BATCH_SIZE==0:
            with open(os.path.join(TARGET_PATH, 'item_{}.json'.format(int((x+1)/RESULT_BATCH_SIZE))), 'w') as f:
                json.dump(item_list, f, indent=4, separators=(', ', ': '))
            item_list = []

    except StopIteration:
        print("StopIteration_Raised")
        with open(os.path.join(TARGET_PATH, 'item_{}.json'.format(int((x+1)/RESULT_BATCH_SIZE + 1))), 'w') as f:
            json.dump(item_list, f, indent=4, separators=(', ', ': '))
        item_list = []

file.close()
