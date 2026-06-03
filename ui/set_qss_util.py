# -*- coding: utf-8 -*-
"""
SuperPicky - UI QSS 函数定义
极简艺术风格 (Minimalist Artistic Design)
"""
from PySide6.QtWidgets import QPushButton,QCheckBox,QComboBox
from ui.styles import COLORS, FONTS

def update_toogle_btn_style(focus_btn: QPushButton, visible: bool) -> None:
    """visible=True → accent 激活色；False → 灰色 secondary 样式。"""
    if visible:
        focus_btn.setStyleSheet(
            f"QPushButton {{ background-color: {COLORS['bg_input']};"
            f" border: 1px solid {COLORS['accent']};"
            f" border-radius: 6px;"
            f" color: {COLORS['accent']};"
            f" font-size: 12px;"
            f" padding: 2px 10px; }}"
        )
    else:
        focus_btn.setStyleSheet(
            f"QPushButton {{ background-color: {COLORS['bg_card']};"
            f" border: 1px solid {COLORS['border']};"
            f" border-radius: 6px;"
            f" color: {COLORS['text_secondary']};"
            f" font-size: 12px;"
            f" padding: 2px 10px; }}"
        )

def set_btn_style(btn: QPushButton):
    #background-color: #00e6b8;
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['accent_light']};
            border-radius: 6px;
            color: {COLORS['accent']};
            font-size: 13px;
            padding: 2px 10px;
        }}
        QPushButton:hover {{
            color: #ffffff;
            border: 1px solid {COLORS['accent_deep']};
        }}
    """)

def set_checkbox_style(checkbox:QCheckBox,color=""):
    """公共工具函数：统一设置 QCheckBox 样式"""
    if color:
        checkbox.setStyleSheet(f"""
             QCheckBox {{
                 color: {color};
                 font-size: 12px;
                 spacing: 4px;
             }}
             QCheckBox::indicator {{
                 width: 14px;
                 height: 14px;
                 border-radius: 3px;
                 border: 1px solid {COLORS['border']};
                 background: transparent;
             }}
             QCheckBox::indicator:checked {{
                 background-color: {color};
                 border-color: {color};
             }}
         """)
    else:
        checkbox.setStyleSheet(f"""
             QCheckBox {{
                 color: {COLORS['text_secondary']};
                 font-size: 12px;
                 spacing: 4px;
             }}
             QCheckBox::indicator {{
                 width: 14px;
                 height: 14px;
                 border-radius: 3px;
                 border: 1px solid {COLORS['border']};
                 background: transparent;
             }}
             QCheckBox::indicator:checked {{
                 background-color: {COLORS['accent']};
                 border-color: {COLORS['accent']};
             }}
         """)

def set_combobox_style(combobox:QComboBox):
    combobox.setStyleSheet(f"""
        QComboBox {{
            background-color: {COLORS['bg_input']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 6px 12px;
            color: {COLORS['text_primary']};
            font-size: 13px;
        }}
        QComboBox:hover {{ border-color: {COLORS['text_muted']}; }}
        QComboBox:focus {{ border-color: {COLORS['accent']}; }}
        QComboBox::drop-down {{ border: none; width: 20px; }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['bg_elevated']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['accent_dim']};
            selection-color: {COLORS['accent']};
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 6px 12px;
            min-height: 24px;
        }}
    """)