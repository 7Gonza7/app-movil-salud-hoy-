# -*- coding: utf-8 -*-

# --- IMPORTANTE: configurar tamaño ANTES de crear la ventana ---
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '320')
Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'resizable', '1')

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import DictProperty, StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from datetime import date, timedelta
import os

from kivy.utils import platform
# (ya no necesitamos tocar Window directamente)
from kivy.metrics import dp

# Importar el módulo de base de datos
from .database import Database
from .auth_database import AuthDatabase
from .session_manager import SessionManager


def today_key():
    return date.today().isoformat()


def last_n_days(n=7):
    base = date.today()
    return [(base - timedelta(days=i)).isoformat() for i in range(n)][::-1]


class SaludHoyApp(MDApp):
    user_data = DictProperty({})
    consejo_del_dia = StringProperty("")
    is_loading = BooleanProperty(False)

    # Instancia de base de datos
    db = None
    
    # Instancias de autenticación
    auth_db = None
    session_manager = None
    current_user = None
    
    # Contador para rotar consejos
    current_tip_index = 0

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

    def build(self):
        self.title = "Salud Hoy"

        # Tema: verde oscuro + texto negro
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"

        return Builder.load_file(os.path.join(os.path.dirname(__file__), "salud_hoy.kv"))

    def on_start(self):
        # Inicializar base de datos SQLite en el proyecto (data/salud_hoy.db)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "data", "salud_hoy.db")
        self.db = Database(db_path)
        
        # Inicializar base de datos de autenticación
        auth_db_path = os.path.join(project_root, "data", "users.db")
        self.auth_db = AuthDatabase(auth_db_path)
        
        # Inicializar gestor de sesiones
        self.session_manager = SessionManager()
        
        # Verificar si hay una sesión activa
        saved_session = self.session_manager.load_session()
        if saved_session:
            # Verificar que el usuario aún existe en la BD
            user = self.auth_db.get_user_by_email(saved_session.get("email", ""))
            if user:
                self.current_user = user
                # Ir directamente a la pantalla principal
                self.root.ids.screen_manager.current = "main"
                self._load_data()
                self._ensure_today_structure()
                self._set_consejo_del_dia()
                Clock.schedule_once(lambda *_: self.refresh_ui(), 0.1)
                toast(f"¡Bienvenido de nuevo, {user['name']}!")
            else:
                # Sesión inválida, limpiar y mostrar login
                self.session_manager.clear_session()
                self.root.ids.screen_manager.current = "login"
        else:
            # No hay sesión, mostrar login
            self.root.ids.screen_manager.current = "login"

    # ---------- DATA ----------
    def _load_data(self):
        """Carga datos del perfil desde la base de datos"""
        profile = self.db.get_profile()
        self.user_data = {
            "profile": profile,
            "days": {}  # Ya no usamos esto, pero lo mantenemos por compatibilidad
        }

    def _ensure_today_structure(self):
        """Asegura que existe el día de hoy en la base de datos"""
        dkey = today_key()
        self.db.ensure_day_exists(dkey)

    # ---------- CONSEJO ----------
    def _set_consejo_del_dia(self):
        if not self.TIP_LIST:
            self.consejo_del_dia = "Hoy es un buen día para cuidarte."
            return
        # Establecer el índice inicial basado en el día
        self.current_tip_index = date.today().toordinal() % len(self.TIP_LIST)
        self.consejo_del_dia = self.TIP_LIST[self.current_tip_index]

    def refresh_daily_tip(self):
        if not self.TIP_LIST:
            return
        # Avanzar al siguiente consejo en la lista
        self.current_tip_index = (self.current_tip_index + 1) % len(self.TIP_LIST)
        self.consejo_del_dia = self.TIP_LIST[self.current_tip_index]
        
        # Forzar actualización de la UI
        Clock.schedule_once(lambda *_: self._update_tip_ui(), 0)

    def _update_tip_ui(self):
        """Actualiza la UI del consejo del día"""
        try:
            if hasattr(self.root.ids, 'lbl_tip'):
                self.root.ids.lbl_tip.text = self.consejo_del_dia
        except Exception as e:
            print(f"Error actualizando UI del consejo: {e}")

    # ---------- HÁBITOS ----------
    def refresh_ui(self):
        self.is_loading = True
        dkey = today_key()
        habits_today = self.db.get_day_habits(dkey)
        ids = self.root.ids

        mapping = [("ck_camina","camina_10"),("ck_estira","estirate_2"),
                   ("ck_respira","respira_1"),("ck_postura","postura_1")]
        for _id, key in mapping:
            if _id in ids:
                ids[_id].active = habits_today.get(key, False)

        # Actualizar el consejo del día en la UI
        self._update_tip_ui()
        
        self._update_today_counter()
        self._build_badges_ui()
        self.is_loading = False

    def on_toggle_habit(self, key, active):
        if self.is_loading:
            return
        dkey = today_key()
        self.db.set_habit_status(dkey, key, bool(active))
        self._update_today_counter()
        self._build_badges_ui()

    def _update_today_counter(self):
        dkey = today_key()
        done = self.db.get_completed_count_for_day(dkey)
        total = len(self.HABITS)
        if "lbl_today_progress" in self.root.ids:
            self.root.ids.lbl_today_progress.text = f"Completados hoy: {done}/{total}"

    # === Métricas para medallas ===
    def _day_score(self, day_date):
        """Calcula el score de un día específico basado en hábitos completados"""
        return self.db.get_completed_count_for_day(day_date)

    def _current_streak(self, threshold=1):
        """Calcula la racha actual desde la base de datos"""
        return self.db.get_streak(threshold)

    def _weekly_score(self):
        """Calcula el score de la última semana"""
        total = 0
        for day_str in last_n_days(7):
            total += self.db.get_completed_count_for_day(day_str)
        return total

    def _active_days_this_month(self):
        """Calcula los días activos del mes actual"""
        today = date.today()
        return self.db.get_monthly_active_days(today.year, today.month)

    def _compute_badges(self):
        streak = self._current_streak(threshold=1)
        weekly = self._weekly_score()
        active_month = self._active_days_this_month()

        today_score = self._day_score(today_key())
        today_full = today_score == len(self.HABITS)
        
        # Verificar si alguna vez ha estado activo
        all_days = self.db.get_all_days_with_habits()
        ever_active = len(all_days) > 0

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

    def _build_badges_ui(self):
        ids = self.root.ids
        if "badges_grid" not in ids:
            return

        from kivymd.uix.chip import MDChip
        badges, streak, weekly, active_month = self._compute_badges()

        if "badge_chips" in ids:
            chips_box = ids.badge_chips
            chips_box.clear_widgets()
            for text in (f"Racha: {streak} día(s)", f"Semana: {weekly}/28", f"Activos mes: {active_month}"):
                chip = MDChip(text=text)
                chip.md_bg_color = (0, 0.6, 0.3, 0.12)
                chip.text_color = (0, 0.45, 0.25, 1)
                chips_box.add_widget(chip)

        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.label import MDIcon

        grid = ids.badges_grid
        grid.clear_widgets()

        GREEN = (0, 0.6, 0.3, 1)
        GREY = (0.68, 0.68, 0.68, 1)

        for b in badges:
            tile = MDBoxLayout(
                orientation="vertical",
                spacing="4dp",
                padding=[0, dp(4), 0, dp(4)],
                size_hint=(1, None),
                height=dp(90),
            )
            icon = MDIcon(
                icon=b["icon"],
                theme_text_color="Custom",
                text_color=GREEN if b["unlocked"] else GREY,
                font_size="28sp",
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
        from kivymd.uix.button import MDFlatButton, MDRaisedButton
        from kivymd.uix.label import MDLabel, MDIcon
        from kivymd.uix.card import MDSeparator
        from kivy.uix.widget import Widget

        # Contenedor principal con diseño mejorado
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(16),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        # Contenedor horizontal para ícono + título
        title_container = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(40),
        )
        
        # Ícono decorativo
        icon = MDIcon(
            icon="account-edit",
            theme_text_color="Custom",
            text_color=(0.1, 0.37, 0.13, 1),  # Verde #1B5E20
            font_size="32sp",
            size_hint_x=None,
            width=dp(32),
            pos_hint={"center_y": 0.5},
        )
        title_container.add_widget(icon)
        
        # Título del diálogo
        title_label = MDLabel(
            text="Editar Perfil",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0.1, 0.37, 0.13, 1),  # Verde #1B5E20
            halign="left",
            valign="center",
            bold=True,
        )
        title_container.add_widget(title_label)
        
        content.add_widget(title_container)

        # Separador decorativo
        separator = MDSeparator(
            color=(0.9, 0.9, 0.9, 1),
        )
        content.add_widget(separator)

        # Espaciador
        content.add_widget(Widget(size_hint_y=None, height=dp(16)))

        # Campo de nombre mejorado
        name_input = MDTextField(
            hint_text="Tu nombre",
            text=self.user_data.get("profile", {}).get("name", ""),
            helper_text="¿Cómo quieres que te llame?",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height=dp(68),
            font_size="16sp",
            line_color_focus=(0.1, 0.37, 0.13, 1),  # Verde #1B5E20
        )
        content.add_widget(name_input)

        # Campo de objetivo mejorado
        goal_input = MDTextField(
            hint_text="Tu objetivo personal",
            text=self.user_data.get("profile", {}).get("goal", "Moverme más"),
            helper_text="Ej: Moverme más, Comer saludable, Dormir mejor",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height=dp(68),
            font_size="16sp",
            line_color_focus=(0.1, 0.37, 0.13, 1),  # Verde #1B5E20
        )
        content.add_widget(goal_input)

        # Espaciador antes de los botones
        content.add_widget(Widget(size_hint_y=None, height=dp(12)))

        def save_and_close(*_):
            try:
                name = name_input.text.strip()
                goal = goal_input.text.strip() or "Moverme más"
                
                # Guardar en base de datos
                self.db.update_profile(name, goal)
                
                # Actualizar datos en memoria
                self.user_data["profile"]["name"] = name
                self.user_data["profile"]["goal"] = goal
                
                self.refresh_profile_labels()
                dialog.dismiss()
                toast("✓ Perfil actualizado")
            except Exception as e:
                print(f"[ERROR] Error al guardar perfil: {e}")
                toast("Error al guardar")

        # Botones mejorados
        cancel_button = MDFlatButton(
            text="CANCELAR",
            theme_text_color="Custom",
            text_color=(0.46, 0.46, 0.46, 1),  # Gris #757575
            on_release=lambda *_: dialog.dismiss(),
        )
        
        save_button = MDRaisedButton(
            text="GUARDAR",
            md_bg_color=(0.1, 0.37, 0.13, 1),  # Verde #1B5E20
            text_color=(1, 1, 1, 1),  # Blanco
            elevation=4,
            on_release=save_and_close,
        )

        dialog = MDDialog(
            type="custom",
            content_cls=content,
            buttons=[cancel_button, save_button],
            auto_dismiss=False,
            size_hint=(None, None),
            width=dp(350),
            radius=[16, 16, 16, 16],
            elevation=8,
            md_bg_color=(1, 1, 1, 1),  # Blanco
        )
        dialog.open()

    def refresh_profile_labels(self):
        ids = self.root.ids
        profile = self.user_data.get("profile", {})
        if "lbl_name" in ids:
            ids.lbl_name.text = profile.get("name", "") or "Sin nombre"
        if "lbl_goal" in ids:
            ids.lbl_goal.text = profile.get("goal", "Moverme más")

    def open_drawer(self):
        self.root.ids.nav_drawer.set_state("open")

    def reset_data(self):
        """Resetea todos los datos de la aplicación"""
        self.db.reset_all_data()
        self._load_data()
        self._ensure_today_structure()
        self.refresh_ui()
        toast("Datos restaurados")

    def switch_tab(self, name):
        self.root.ids.bottom_nav.switch_tab(name)
        if name == "profile":
            Clock.schedule_once(lambda *_: self.refresh_profile_labels(), 0.05)

    # ---------- AUTENTICACIÓN ----------
    def do_login(self):
        """Maneja el inicio de sesión"""
        email = self.root.ids.login_email.text.strip()
        password = self.root.ids.login_password.text
        
        # Validar campos
        if not email or not password:
            toast("Por favor, completa todos los campos")
            return
        
        # Verificar credenciales
        user = self.auth_db.check_user(email, password)
        
        if user:
            # Login exitoso
            self.current_user = user
            self.session_manager.save_session(user)
            
            # Limpiar campos
            self.root.ids.login_email.text = ""
            self.root.ids.login_password.text = ""
            
            # Cargar datos y ir a la pantalla principal
            self._load_data()
            self._ensure_today_structure()
            self._set_consejo_del_dia()
            self.root.ids.screen_manager.current = "main"
            Clock.schedule_once(lambda *_: self.refresh_ui(), 0.1)
            toast(f"✓ Bienvenido, {user['name']}!")
        else:
            # Credenciales incorrectas
            toast("✗ Email o contraseña incorrectos")
    
    def do_register(self):
        """Maneja el registro de nuevos usuarios"""
        name = self.root.ids.register_name.text.strip()
        email = self.root.ids.register_email.text.strip()
        password = self.root.ids.register_password.text
        
        # Validar campos
        if not name or not email or not password:
            toast("Por favor, completa todos los campos")
            return
        
        # Validar email
        if "@" not in email or "." not in email:
            toast("Por favor, ingresa un email válido")
            return
        
        # Validar contraseña
        if len(password) < 6:
            toast("La contraseña debe tener al menos 6 caracteres")
            return
        
        # Intentar registrar
        success = self.auth_db.add_user(name, email, password)
        
        if success:
            # Registro exitoso
            # Limpiar campos
            self.root.ids.register_name.text = ""
            self.root.ids.register_email.text = ""
            self.root.ids.register_password.text = ""
            
            # Ir al login
            self.root.ids.screen_manager.current = "login"
            toast(f"✓ Cuenta creada exitosamente. ¡Inicia sesión!")
        else:
            # Email ya existe
            toast("✗ Este email ya está registrado")
    
    def logout(self):
        """Cierra la sesión actual"""
        self.session_manager.clear_session()
        self.current_user = None
        
        # Limpiar campos de login
        self.root.ids.login_email.text = ""
        self.root.ids.login_password.text = ""
        
        # Ir a la pantalla de login
        self.root.ids.screen_manager.current = "login"
        toast("✓ Sesión cerrada")
    
    def go_to_login(self):
        """Navega a la pantalla de login"""
        self.root.ids.screen_manager.current = "login"
    
    def go_to_register(self):
        """Navega a la pantalla de registro"""
        self.root.ids.screen_manager.current = "register"

    def on_stop(self):
        """Cierra la conexión a la base de datos al cerrar la app"""
        if self.db:
            self.db.close()
        return True


if __name__ == "__main__":
    SaludHoyApp().run()
