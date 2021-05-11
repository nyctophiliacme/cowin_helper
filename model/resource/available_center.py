
class AvailableCenter:
    def __init__(self, center_id, center_name, center_district, center_block_name, center_address, center_pincode,
                 available_dates):
        self.center_id = center_id
        self.center_name = center_name
        self.center_district = center_district
        self.center_block_name = center_block_name
        self.center_address = center_address
        self.center_pincode = center_pincode
        self.available_dates = available_dates

    def print_available_center(self):
        print(self.__dict__)
