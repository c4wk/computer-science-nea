class ItemContainer:
    def __init__(self, game, world, rows, columns):
        self._data = [[None for x in range(columns)] for row_index in range(rows)] # Static size
        self._game = game
        self._world = world
        self._dimensions = (rows, columns)

    @property
    def data(self):
        return self._data

    def get_item(self, row_index, column_index):
        if 0 <= row_index <= len(self._data)-1 and 0 <= column_index <= len(self._data[0])-1:
            return self._data[row_index, column_index]

    def pickup_item(self, item_to_pickup, capacity_check=False):
        if capacity_check and self.get_remaining_capacity_of_same_type(item_to_pickup) < item_to_pickup.quantity:
            print("Not enough capacity to pickup all")

        unfilled_items_list = self.get_unfilled_items_of_same_type(item_to_pickup)
        if len(unfilled_items_list) > 0:
            print("CASE 1")
            item_with_highest_quantity = unfilled_items_list[0]
            for item in unfilled_items_list:
                if item.quantity > item_with_highest_quantity.quantity:
                    item_with_highest_quantity = item
            remaining_quantity = item_with_highest_quantity.max_quantity - item_with_highest_quantity.quantity
            if item_to_pickup.quantity > remaining_quantity :
                item_with_highest_quantity.quantity += remaining_quantity
                item_to_pickup.quantity -= remaining_quantity
                self.pickup_item(item, capacity_check)
            elif item_to_pickup.quantity <= remaining_quantity:
                item_with_highest_quantity.quantity += item_to_pickup.quantity
                item_to_pickup.quantity = 0
        elif self.empty_item_exists():
            print("CASE 2")
            row_index, item_index = self.get_empty_item_indexes()[0]
            self._data[row_index][item_index] = item_to_pickup
        else:
            print("CASE 3")
            return item_to_pickup

    def get_remaining_capacity_of_same_type(self, item_to_check):
        total = 0
        list_of_same_items = self.get_unfilled_items_of_same_type(item_to_check)
        for item in list_of_same_items:
            total += (item.max_quantity - item.quantity)

        for item_to_check in self.get_empty_item_indexes():
            total += item_to_check.max_quantity

        return total

    def get_empty_item_indexes(self):
        indexes = []
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is None:
                    indexes.append((row_index, item_index))
        return indexes


    def empty_item_exists(self):
        for row in self._data:
            for item in row:
                if item is None:
                    return True
        return False

    def get_unfilled_items_of_same_type(self, item_to_check):
        unfilled_items_list = []
        for row in self._data:
            for item in row:
                if item is not None:
                    if item.item_id == item_to_check.item_id and item.quantity < item.max_quantity:
                        print("Unfilled item added for return")
                        unfilled_items_list.append(item)

        return unfilled_items_list
    
    def convert_data(self):
        data = \
        {
            "container_id": "item_container",
            "state_data": self.get_state_data()
        }
        return data

    def load_from_data(self, data):
        self._data.clear()
        print(f"data:{self._data}")
        self._dimensions = (len(data), len(data[0]))
        self._data = [[None for column_index in range(self._dimensions[1])] for row_index in range(self._dimensions[0])]

        for row_index, row in enumerate(data):
            print(f"ROW INDEX :{row_index}")
            self._data.append([])
            for item_index, item in enumerate(row):
                if item is not None:
                    self._data[row_index][item_index] = self._game.item_factory.create_item(self._game, self._world, item["item_id"], item["state_data"])
                else:
                    self._data[row_index][item_index] = None

    def get_state_data(self):
        data = [[None for x in range(self._dimensions[1])] for y in range(self._dimensions[0])]
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is not None:
                    data[row_index][item_index] = item.convert_data()
                else:
                    data[row_index][item_index] = None
        return data

    def update(self):
        for row_index, row in enumerate(self._data):
            for item_index, item in enumerate(row):
                if item is not None:
                    if item.quantity == 0:
                        self._data[row_index][item_index] = None



