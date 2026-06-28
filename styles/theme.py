class Theme:
    LIGHT = {
        'bg': '#f0f0f0',
        'fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'button_bg': '#007bff',
        'button_fg': '#ffffff',
        'listbox_bg': '#ffffff',
        'listbox_fg': '#000000',
        'select_bg': '#007bff',
        'select_fg': '#ffffff',
        'success': '#28a745',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8'
    }
    
    DARK = {
        'bg': '#1e1e1e',
        'fg': '#ffffff',
        'entry_bg': '#2d2d2d',
        'entry_fg': '#ffffff',
        'button_bg': '#0d6efd',
        'button_fg': '#ffffff',
        'listbox_bg': '#2d2d2d',
        'listbox_fg': '#ffffff',
        'select_bg': '#0d6efd',
        'select_fg': '#ffffff',
        'success': '#198754',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#0dcaf0'
    }
    
    current_theme = 'dark'
    
    @classmethod
    def get(cls):
        return cls.DARK if cls.current_theme == 'dark' else cls.LIGHT
    
    @classmethod
    def toggle(cls):
        cls.current_theme = 'light' if cls.current_theme == 'dark' else 'dark'
        return cls.get()