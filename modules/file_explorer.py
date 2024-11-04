import os
from core.lcd import FILE, MINUS, PLUS, POINTER
from modules.menu import FeatureItem
from core.beeper import menu_key, jump_melody

class NodeType:
    DIRECTORY = 0
    FILE = 1

class FileExplorer:
    def __init__(self, lcd, buttons, system, beeper):
        self.lcd = lcd
        self.buttons = buttons
        self.system = system
        self.beeper = beeper
        self.root_node = self._scan_directory('')  # Scan the root directory
        self.display_lines = []
        self.current_selection = 0 

    def enter(self):
        self.display_lines = self._generate_display_lines(self.root_node, include_back_option=True)
        self._print_lines()

    def exit(self):
        self.lcd.animated_clear()

    def update(self):
        if self.buttons.is_pressed(self.buttons.up) and self.current_selection > 0:
            self.beeper.play_melody(menu_key)
            self.current_selection -= 1
            self._print_lines()

        if self.buttons.is_pressed(self.buttons.down) and self.current_selection < len(self.display_lines) - 1:
            self.beeper.play_melody(menu_key)
            self.current_selection += 1
            self._print_lines()

        if self.buttons.is_pressed(self.buttons.select):
            self.beeper.play_melody(jump_melody)
            if self.current_selection == 0:
                self.system.switch_to(FeatureItem.MENU)
            else:
                selected_node = self._get_node_by_index(self.root_node, self.current_selection - 1)
                if selected_node['type'] == NodeType.DIRECTORY: # type: ignore
                    selected_node['is_open'] = not selected_node['is_open'] # type: ignore
                    self.display_lines = self._generate_display_lines(self.root_node, include_back_option=True)
                    self.current_selection = min(self.current_selection, len(self.display_lines) - 1)
                else:
                    self.system.switch_to(FeatureItem.DOC, selected_node['path']) # type: ignore
                    return
                self.display_lines = self._generate_display_lines(self.root_node, include_back_option=True)
                self._print_lines()

    def _print_lines(self):
        current_line = self.display_lines[self.current_selection]
        next_line = self.display_lines[self.current_selection + 1] if self.current_selection + 1 < len(self.display_lines) else ""
        self.lcd.display_tree(f"{POINTER} {current_line}", f"  {next_line}")

    def _scan_directory(self, path):
        def _list_directory_contents(current_path, parent_node):
            for entry in os.listdir(current_path):
                full_path = current_path + '/' + entry
                if self._is_folder(full_path):
                    node = {
                        "name": entry,
                        "path": full_path,
                        "type": NodeType.DIRECTORY,
                        "is_open": False,
                        "children": []
                    }
                    parent_node['children'].append(node)
                    _list_directory_contents(full_path, node)  # Recursively list files in the directory
                else:
                    node = {
                        "name": entry,
                        "path": full_path,
                        "type": NodeType.FILE
                    }
                    parent_node['children'].append(node)

        root_node = {
            "name": 'Root',
            "path": '/',
            "type": NodeType.DIRECTORY,
            "is_open": True,
            "children": []
        }
        _list_directory_contents(path, root_node)
        return root_node
    
    def _generate_display_lines(self, node, indent_level=0, include_back_option=False):
        lines = []
        if include_back_option:
            lines.append('Back')  # Add "Back" option only once at the top level
        indent = ' ' * indent_level  # Use the current indent level without adding extra space
        if node['name'] == 'Root':
            level_indicator = MINUS if node['is_open'] else PLUS
            lines.append(f"{level_indicator} {node['name']}")  # Use the current indent level
            if node['is_open']:
                for child in node['children']:
                    lines.extend(self._generate_display_lines(child, indent_level + 1))  # Increased indent level for children
        elif node['type'] == NodeType.DIRECTORY:
            level_indicator = MINUS if node['is_open'] else PLUS
            lines.append(f"{indent}{level_indicator} {node['name']}")
            if node['is_open']:
                for child in node['children']:
                    lines.extend(self._generate_display_lines(child, indent_level + 1))  # Increased indent level for children
        else:
            file_icon = FILE
            lines.append(f"{indent}{file_icon} {node['name']}")
        return lines
    
    def _get_node_by_index(self, node, index, current_index=0):
        if current_index == index:
            return node
        if node['type'] == NodeType.DIRECTORY and node['is_open']:
            for child in node['children']:
                current_index += 1
                result = self._get_node_by_index(child, index, current_index)
                if result:
                    return result
                current_index += len(self._generate_display_lines(child)) - 1
        return None
      
    def _is_folder(self, full_path): 
        return os.stat(full_path)[0] & 0x4000 # Check if it's a directory