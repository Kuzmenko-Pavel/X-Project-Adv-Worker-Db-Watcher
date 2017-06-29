from x_project_adv_worker_db_watcher.utils import Map


class BlockSetting(Map):
    def __init__(self, *args, **kwargs):
        self.width = 0
        self.height = 0
        self.border = 0
        self.border_color = 'white'
        self.background_color = 'transparent'
        self.border_radius = [0, 0, 0, 0]
        self.header = Map()
        self.header.width = 0
        self.header.height = 0
        self.header.top = 0
        self.header.left = 0
        self.footer = Map()
        self.footer.width = 0
        self.footer.height = 0
        self.footer.top = 0
        self.footer.left = 0
        self.default_button = Map()
        self.default_button.block = 'Подробнее'
        self.default_button.ret_block = 'Подробнее'
        self.default_button.rec_block = 'Подробнее'
        self.default_adv = Map()
        self.styling_adv = Map()
        self.default_adv.count_column = 0
        self.default_adv.count_row = 0
        self.default_adv.count_adv = 0
        self.default_adv.width = 0
        self.default_adv.height = 0
        self.default_adv.type = None
        self.styling_adv.count_column = 0
        self.styling_adv.count_row = 0
        self.default_adv.count_adv = 0
        self.styling_adv.width = 0
        self.styling_adv.height = 0
        self.styling_adv.type = None
        super(BlockSetting, self).__init__(*args, **kwargs)
