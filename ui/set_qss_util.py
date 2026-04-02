# -*- coding: utf-8 -*-
"""
SuperPicky - UI QSS 函数定义
极简艺术风格 (Minimalist Artistic Design)
"""
from PySide6.QtWidgets import QPushButton
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
