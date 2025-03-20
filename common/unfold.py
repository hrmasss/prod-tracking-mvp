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
    "BORDER_RADIUS": "5px",
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
            "50": "230 245 255",
            "100": "198 232 255",
            "200": "156 213 255",
            "300": "95 186 252",
            "400": "38 157 248",
            "500": "0 122 230",
            "600": "0 102 217",
            "700": "0 85 191",
            "800": "4 68 155",
            "900": "8 55 120",
            "950": "6 32 78",
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
                        "title": "Production Targets",
                        "icon": "assessment",
                        "link": reverse_lazy(
                            "admin:tracker_productiontarget_changelist"
                        ),
                    },
                    {
                        "title": "Orders",
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:tracker_order_changelist"),
                    },
                    {
                        "title": "Materials",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:tracker_material_changelist"),
                    },
                    {
                        "title": "Styles",
                        "icon": "apparel",
                        "link": reverse_lazy("admin:tracker_style_changelist"),
                    },
                    {
                        "title": "Production Batches",
                        "icon": "inventory",
                        "link": reverse_lazy(
                            "admin:tracker_productionbatch_changelist"
                        ),
                    },
                    {
                        "title": "Bundles",
                        "icon": "box",
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
                    {
                        "title": "Quality Checks",
                        "icon": "verified",
                        "link": reverse_lazy("admin:tracker_qualitycheck_changelist"),
                    },
                    {
                        "title": "Defects",
                        "icon": "report",
                        "link": reverse_lazy("admin:tracker_defect_changelist"),
                    },
                    {
                        "title": "Rework Assignments",
                        "icon": "handyman",
                        "link": reverse_lazy(
                            "admin:tracker_reworkassignment_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}
