# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import DictProperty, StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from datetime import date, timedelta
import os, json, random

from kivy.utils import platform
from kivy.core.window import Window
from kivy.metrics import dp


def today_key():
    return date.today().isoformat()


def last_n_days(n=7):
    base = date.today()
    return [(base - timedelta(days=i)).isoformat() for i in range(n)][::-1]


class SaludHoyApp(MDApp):
    user_data = DictProperty({})
    consejo_del_dia = StringProperty("")
    is_loading = BooleanProperty(False)

    HABITS = [
        {"key": "camina_10", "title": "Camina 10 minutos"},
        {"key": "estirate_2", "title": "Estírate 2 minutos"},
        {"key": "respira_1", "title": "Respira 1 minuto"},
        {"key": "postura_1", "title": "Postura recta 1 minuto"},
    ]

    TIP_LIST = [
        "Levántate y camina 2 minutos cada hora.",
        "Come una fruta hoy.",
        "Evita pantallas 30 min antes de dormir.",
        "Respira profundo 5 veces cuando te estreses.",
        "Toma agua a sorbos durante el día.",
        "Estira cuello y hombros por 60 segundos.",
        "Una caminata corta después de comer ayuda a la digestión.",
        "Duerme y despierta a horas regulares.",
        "Ríe: reduce el estrés y mejora el ánimo.",
        "Mantén una postura neutra cuando estés sentado.",
    ]

    # ----------------- Tips en orden aleatorio cíclico -----------------
    def _new_tip_order(self):
        """Baraja todos los tips y guarda un orden cíclico sin repetir."""
        self._tip_order = list(range(len(self.TIP_LIST)))
        random.shuffle(self._tip_order)
        self._tip_pos = 0

    def refresh_daily_tip(self):
        """Siguiente tip según el orden aleatorio; al terminar, vuelve a barajar."""
        if not self.TIP_LIST:
            return
        if not hasattr(self, "_tip_order") or self._tip_pos >= len(self._tip_order):
            self._new_tip_order()
        idx = self._tip_order[self._tip_pos]
        self._tip_pos += 1
        self.consejo_del_dia = self.TIP_LIST[idx]
    # -------------------------------------------------------------------

    def build(self):
        self.title = "Salud Hoy"

        # Ventana tipo teléfono en escritorio: set mínimos ANTES del size
        if platform not in ("android", "ios"):
            Window.minimum_width = 320
            Window.minimum_height = 600
            Window.size = (390, 780)

        # Tema
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"

        kv_path = os.path.join(os.path.dirname(__file__), "salud_hoy.kv")
        return Builder.load_file(kv_path)

    def on_start(self):
        # Datos persistentes en carpeta del usuario
        self.data_file = os.path.join(self.user_data_dir, "salud_hoy_data.json")
        self._ensure_data_file()
        self._load_data()
        self._ensure_today_structure()

        # Tip inicial (usa el sistema cíclico)
        self._new_tip_order()
        self.refresh_daily_tip()

        Clock.schedule_once(lambda *_: self._safe_refresh(), 0)

    def _safe_refresh(self):
        try:
            self.refresh_ui()
        except Exception as e:
            import traceback, sys
            print("ERROR en refresh_ui:", e, file=sys.stderr)
            traceback.print_exc()

    # ---------- DATA ----------
    def _ensure_data_file(self):
        folder = os.path.dirname(self.data_file)
        os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.data_file):
            default = {"profile": {"name": "", "goal": "Moverme más"}, "days": {}}
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(default, f, ensure_ascii=False, indent=2)

    def _load_data(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            self.user_data = json.load(f)

    def _save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.user_data, f, ensure_ascii=False, indent=2)

    def _ensure_today_structure(self):
        dkey = today_key()
        days = self.user_data.setdefault("days", {})
        if dkey not in days:
            days[dkey] = {"habits": {h["key"]: False for h in self.HABITS}}
            self._save_data()

    # ---------- HÁBITOS / MEDALLAS ----------
    def refresh_ui(self):
        self.is_loading = True
        dkey = today_key()
        today = self.user_data.get("days", {}).get(dkey, {"habits": {}})
        habits_today = today.get("habits", {})
        ids = self.root.ids

        for _id, key in [
            ("ck_camina", "camina_10"),
            ("ck_estira", "estirate_2"),
            ("ck_respira", "respira_1"),
            ("ck_postura", "postura_1"),
        ]:
            if _id in ids:
                ids[_id].active = habits_today.get(key, False)

        self._update_today_counter()
        self._build_badges_ui()
        self.is_loading = False

    def on_toggle_habit(self, key, active):
        if self.is_loading:
            return
        dkey = today_key()
        self.user_data["days"].setdefault(dkey, {"habits": {}})
        self.user_data["days"][dkey]["habits"][key] = bool(active)
        self._save_data()
        self._update_today_counter()
        self._build_badges_ui()

    def _update_today_counter(self):
        dkey = today_key()
        habits = self.user_data["days"].get(dkey, {}).get("habits", {})
        total = len(self.HABITS)
        done = sum(1 for k in habits if habits.get(k))
        if "lbl_today_progress" in self.root.ids:
            self.root.ids.lbl_today_progress.text = f"Completados hoy: {done}/{total}"

    # === Métricas para medallas ===
    def _day_score(self, habits):
        return sum(1 for h in self.HABITS if habits.get(h["key"], False))

    def _current_streak(self, threshold=1):
        days = self.user_data.get("days", {})
        d = date.today()
        streak = 0
        while True:
            key = d.isoformat()
            s = self._day_score(days.get(key, {}).get("habits", {}))
            if s >= threshold:
                streak += 1
                d -= timedelta(days=1)
            else:
                break
        return streak

    def _weekly_score(self):
        total = 0
        for k in last_n_days(7):
            h = self.user_data.get("days", {}).get(k, {}).get("habits", {})
            total += self._day_score(h)
        return total

    def _active_days_this_month(self):
        days = self.user_data.get("days", {})
        first = date.today().replace(day=1)
        cur = first
        active = 0
        while cur.month == first.month:
            s = self._day_score(days.get(cur.isoformat(), {}).get("habits", {}))
            if s >= 1:
                active += 1
            cur += timedelta(days=1)
        return active

    def _compute_badges(self):
        streak = self._current_streak(threshold=1)
        weekly = self._weekly_score()
        active_month = self._active_days_this_month()

        today_h = self.user_data.get("days", {}).get(today_key(), {}).get("habits", {})
        today_full = self._day_score(today_h) == len(self.HABITS)
        ever_active = any(
            self._day_score(d.get("habits", {})) >= 1
            for d in self.user_data.get("days", {}).values()
        )

        BADGES = [
            {"key": "first_active", "icon": "check-decagram", "title": "Primer día\nactivo",
             "unlocked": ever_active},
            {"key": "streak_3", "icon": "run", "title": "3 días\nseguidos",
             "unlocked": streak >= 3},
            {"key": "streak_7", "icon": "fire", "title": "7 días\nseguidos",
             "unlocked": streak >= 7},
            {"key": "week_14", "icon": "target", "title": "Semana\n14+",
             "unlocked": weekly >= 14},
            {"key": "week_perfect", "icon": "crown", "title": "Semana\nperfecta",
             "unlocked": weekly == 28},
            {"key": "today_full", "icon": "medal", "title": "Hoy\n4/4",
             "unlocked": today_full},
            {"key": "month_15", "icon": "calendar-check", "title": "15+ días\ndel mes",
             "unlocked": active_month >= 15},
        ]
        return BADGES, streak, weekly, active_month

    # --- Responsividad de chips de resumen ---
    def _adjust_badge_chip_cols(self, *_):
        """Ajusta columnas del grid de chips según ancho para evitar cortes."""
        try:
            grid = self.root.ids.badge_chips
        except Exception:
            return
        w = grid.width
        if w < dp(380):
            cols = 1
        elif w < dp(620):
            cols = 2
        else:
            cols = 3
        if getattr(grid, "cols", 3) != cols:
            grid.cols = cols

    def _build_badges_ui(self):
        ids = self.root.ids
        if "badges_grid" not in ids:
            return

        from kivymd.uix.chip import MDChip
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.label import MDIcon

        badges, streak, weekly, active_month = self._compute_badges()

        # ---- Resumen (chips en grid responsivo) ----
        if "badge_chips" in ids:
            chips_grid = ids.badge_chips
            chips_grid.clear_widgets()
            chips_grid.spacing = dp(8)
            chips_grid.padding = [0, dp(6), 0, dp(6)]

            for text in (f"Racha: {streak} día(s)",
                         f"Semana: {weekly}/28",
                         f"Activos mes: {active_month}"):
                chip = MDChip(text=text)
                chip.md_bg_color = (0, 0.6, 0.3, 0.12)
                chip.text_color   = (0, 0.45, 0.25, 1)
                chip.size_hint_x  = 1  # ocupa el ancho de su celda
                chips_grid.add_widget(chip)

            # Bind responsivo (una sola vez)
            if not getattr(self, "_chips_bound", False):
                chips_grid.bind(width=self._adjust_badge_chip_cols)
                self._chips_bound = True
            self._adjust_badge_chip_cols()

        # ---- Tarjetas de medallas ----
        grid = ids.badges_grid
        grid.clear_widgets()

        GREEN = (0, 0.6, 0.3, 1)
        GREY  = (0.68, 0.68, 0.68, 1)

        for b in badges:
            tile = MDBoxLayout(
                orientation="vertical",
                spacing="6dp",
                padding=[0, dp(6), 0, dp(6)],
                size_hint=(1, None),
                height=dp(110),
            )
            icon = MDIcon(
                icon=b["icon"],
                theme_text_color="Custom",
                text_color=GREEN if b["unlocked"] else GREY,
                font_size="32sp",
                halign="center",
            )
            title = MDLabel(
                text=b["title"],
                halign="center",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                size_hint_y=None,
                text_size=(0, None),
            )
            title.bind(
                width=lambda inst, w: setattr(inst, "text_size", (w, None)),
                texture_size=lambda inst, ts: setattr(inst, "height", ts[1]),
            )
            tile.add_widget(icon)
            tile.add_widget(title)
            grid.add_widget(tile)

    # ---------- PERFIL ----------
    def open_edit_profile(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDFlatButton
        from kivy.uix.widget import Widget

        content = MDBoxLayout(
            orientation="vertical",
            padding="16dp",
            spacing="12dp",
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        name_input = MDTextField(
            hint_text="Nombre",
            text=self.user_data.get("profile", {}).get("name", ""),
            helper_text="Cómo quieres que te llame la app",
            helper_text_mode="on_focus",
        )
        goal_input = MDTextField(
            hint_text="Objetivo (ej. Moverme más)",
            text=self.user_data.get("profile", {}).get("goal", "Moverme más"),
            helper_text="Un objetivo corto y claro",
            helper_text_mode="on_focus",
        )
        for tf in (name_input, goal_input):
            tf.size_hint_y = None
            tf.height = dp(56)

        content.add_widget(name_input)
        content.add_widget(goal_input)
        content.add_widget(Widget(size_hint_y=None, height=dp(8)))

        def save_and_close(*_):
            self.user_data.setdefault("profile", {})
            self.user_data["profile"]["name"] = name_input.text.strip()
            self.user_data["profile"]["goal"] = goal_input.text.strip() or "Moverme más"
            self._save_data()
            self.refresh_profile_labels()
            dialog.dismiss()
            toast("Perfil actualizado")

        dialog = MDDialog(
            title="Editar perfil",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda *_: dialog.dismiss()),
                MDFlatButton(text="Guardar", on_release=save_and_close),
            ],
            auto_dismiss=False,
        )
        dialog.open()

    def refresh_profile_labels(self):
        ids = self.root.ids
        profile = self.user_data.get("profile", {})
        if "lbl_name" in ids:
            ids.lbl_name.text = profile.get("name", "") or "Sin nombre"
        if "lbl_goal" in ids:
            ids.lbl_goal.text = profile.get("goal", "Moverme más")

    # ---------- NAV ----------
    def open_drawer(self):
        self.root.ids.nav_drawer.set_state("open")

    def reset_data(self):
        self.user_data = {"profile": {"name": "", "goal": "Moverme más"}, "days": {}}
        self._save_data()
        self._ensure_today_structure()
        self.refresh_ui()
        toast("Datos restaurados")

    def switch_tab(self, name):
        self.root.ids.bottom_nav.switch_tab(name)
        if name == "profile":
            Clock.schedule_once(lambda *_: self.refresh_profile_labels(), 0.05)


if __name__ == "__main__":
    SaludHoyApp().run()
