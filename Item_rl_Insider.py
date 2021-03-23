class Item_rl_Insider:
    def __init__(self, item_name, item_url_name, item_rarity, item_type, item_is_paintable, item_price_list):
        self.name = item_name
        self.url_name = item_url_name
        self.rarity = item_rarity
        self.type = item_type
        self.is_paintable = item_is_paintable
        # order:
        # default, black, white, grey, crimson, pink, cobalt, sky blue, sienna, saffron, lime, green, orange, purple
        self.price_list = item_price_list
