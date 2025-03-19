from django.urls import reverse_lazy
from django.templatetags.static import static


UNFOLD_CONFIG = {
    "SITE_TITLE": "Production Tracking Admin",
    "SITE_HEADER": "Production Tracking",
    "SITE_SYMBOL": "barcode",
    "THEME": "light",
    "STYLES": [
        lambda request: static("css/admin.styles.css"),
    ],
    "BORDER_RADIUS": "10px",
    "COLORS": {
        "base": {
            "50": "250 250 250",
            "100": "244 245 246",
            "200": "228 230 232",
            "300": "212 215 218",
            "400": "176 181 186",
            "500": "136 141 147",
            "600": "102 107 114",
            "700": "78 83 90",
            "800": "54 58 65",
            "900": "34 38 45",
            "950": "18 20 26",
        },
        "primary": {
            "50": "226 239 247",
            "100": "192 217 236",
            "200": "148 188 221",
            "300": "104 159 206",
            "400": "61 130 191",
            "500": "5 75 121",
            "600": "4 66 107",
            "700": "3 55 90",
            "800": "3 44 73",
            "900": "2 36 60",
            "950": "1 22 39",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Authentication & Users",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "group",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": "Departments",
                        "icon": "apartment",
                        "link": reverse_lazy("admin:users_department_changelist"),
                    },
                    {
                        "title": "Roles",
                        "icon": "badge",
                        "link": reverse_lazy("admin:users_role_changelist"),
                    },
                ],
            },
            {
                "title": "Production Tracking",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Styles",
                        "icon": "apparel",
                        "link": reverse_lazy("admin:tracker_style_changelist"),
                    },
                    {
                        "title": "Bundles",
                        "icon": "package",
                        "link": reverse_lazy("admin:tracker_bundle_changelist"),
                    },
                    {
                        "title": "Production Lines",
                        "icon": "factory",
                        "link": reverse_lazy("admin:tracker_productionline_changelist"),
                    },
                    {
                        "title": "Scan Events",
                        "icon": "history",
                        "link": reverse_lazy("admin:tracker_scanevent_changelist"),
                    },
                ],
            },
        ],
    },
}
