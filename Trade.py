class Trade:
    def __init__(self, rlg_name, platform, platform_username, platform_link, has_item_list, wants_item_list, trade_time,
                 trade_note):
        self.rlg_name = rlg_name
        self.platform = platform
        self.platform_username = platform_username
        self.platform_link = platform_link
        self.has_item_list = has_item_list
        self.wants_item_list = wants_item_list
        self.time = trade_time
        self.note = trade_note

    def add_trade_content(self, has, wants):
        self.content_list.append([has, wants])
