from modules.menu import FeatureItem

class System:
    def __init__(self, lcd, buttons, menu, doc):
        self.lcd = lcd
        self.buttons = buttons
        self.menu = menu
        self.doc = doc
        self.current_feature = None  # Holds the active feature
        self.feature_history = []

    def switch_to(self, feature, file_path=None):
        # Switch from the current feature to a new one.
        if self.current_feature:
            self.lcd.reset_custom_chars()
            self.current_feature.exit()  # Exit the previous feature
            self.feature_history.append(self.current_feature)  # Save to history

        if feature == FeatureItem.MENU:
            self.menu.enter()  # Enter the main menu
            self.current_feature = self.menu
        elif feature == FeatureItem.DOC:
            self.doc.enter(file_path)
            self.current_feature = self.doc
        else:
            self.current_feature = feature
            self.current_feature.enter()  # Enter the selected feature
            
    def back(self):
        # Return to the last open feature.
        if self.feature_history:
            last_feature = self.feature_history.pop()
            self.switch_to(last_feature)

    def update(self):
        # Update the active feature.
        if self.current_feature:
            self.current_feature.update()
