class NiftyCloudRegion():

    def __init__(self, region_name, is_default=False):
        self.name = region_name
        self.is_default = is_default

    @classmethod
    def correct_region_name(cls, incomplete_region_name):

        supply_map = {
            'east-1': 'jp-east-1',
            'east-2': 'jp-east-2',
            'east-3': 'jp-east-3',
            'east-4': 'jp-east-4',
            'west-1': 'jp-west-1',
        }

        if incomplete_region_name in supply_map:
            return supply_map[incomplete_region_name]

        return incomplete_region_name
