# ============================================================
# WASEET AL-KHAIR
# NEW BUILD - 11-11 - FIXED
# Android / Kivy / SQLite / Offline First
# Single Python File
# ============================================================

import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# ============================================================
# SETTINGS
# ============================================================

APP_NAME = "WASEET AL-KHAIR"

GREEN = (0.05, 0.45, 0.18, 1)
DARK_GREEN = (0.02, 0.30, 0.11, 1)
RED = (0.85, 0.05, 0.05, 1)
BLUE = (0.03, 0.25, 0.65, 1)
BLACK = (0.05, 0.05, 0.05, 1)
WHITE = (1, 1, 1, 1)
GOLD = (0.95, 0.65, 0.05, 1)

# Change this one value later if the bank incentive changes.
BANK_INCENTIVE_PER_TON = 100.0

# Payment fee = 1%
BANK_FEE_RATE = 0.01


# ============================================================
# CROPS
# ============================================================

CROPS = [
    "Wheat",
    "Corn",
    "Rice",
    "Beans",
    "Fava Beans",
    "Clover",
    "Cotton",
    "Tomato",
    "Potato",
    "Onion",
    "Garlic",
    "Cucumber",
    "Pepper",
    "Eggplant",
    "Carrot",
    "Cabbage",
    "Lettuce",
    "Peas",
    "Okra",
    "Spinach",
    "Molokhia",
    "Zucchini",
    "Broccoli",
    "Cauliflower",
    "Green Beans",
    "Peanuts",
    "Sesame",
    "Sunflower",
    "Sugar Cane",
    "Sugar Beet",
    "Orange",
    "Mandarin",
    "Lemon",
    "Mango",
    "Banana",
    "Grapes",
    "Strawberry",
    "Guava",
    "Peach",
    "Apricot",
    "Plum",
    "Apple",
    "Pear",
    "Pomegranate",
    "Watermelon",
    "Melon",
    "Fig",
    "Date",
    "Olive",
    "Other"
]


# ============================================================
# DATABASE
# ============================================================

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def database_path():
    try:
        app = App.get_running_app()
        return os.path.join(
            app.user_data_dir,
            "waseet_alkhair_new.db"
        )
    except Exception:
        return os.path.join(
            os.path.dirname(__file__),
            "waseet_alkhair_new.db"
        )


def get_connection():
    conn = sqlite3.connect(database_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_database():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT,
            village TEXT,
            area REAL DEFAULT 0,
            crop TEXT,
            quantity REAL DEFAULT 0,
            price_per_ton REAL DEFAULT 0,
            account TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS traders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            village TEXT,
            commercial_register TEXT,
            mobile TEXT,
            account TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            farmer_name TEXT,
            farmer_mobile TEXT,
            farmer_account TEXT,
            trader_id INTEGER,
            trader_name TEXT,
            crop TEXT,
            quantity REAL,
            price_per_ton REAL,
            total_value REAL,
            status TEXT DEFAULT 'SENT',
            paid_amount REAL DEFAULT 0,
            created_at TEXT,
            received_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            trader_id INTEGER,
            trader_name TEXT,
            farmer_id INTEGER,
            farmer_name TEXT,
            farmer_account TEXT,
            amount REAL,
            fee REAL,
            net_amount REAL,
            payment_date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS crop_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT UNIQUE,
            price REAL DEFAULT 0,
            updated_at TEXT
        )
    """)

    conn.commit()

    defaults = {
        "Wheat": 18000,
        "Corn": 17000,
        "Rice": 19000,
        "Beans": 22000,
        "Fava Beans": 22000,
        "Clover": 16000,
        "Cotton": 30000,
        "Tomato": 39000,
        "Potato": 39000,
        "Onion": 30000,
        "Garlic": 45000,
        "Cucumber": 30000,
        "Pepper": 35000,
        "Eggplant": 28000,
        "Carrot": 25000,
        "Cabbage": 22000,
        "Lettuce": 22000,
        "Peas": 30000,
        "Okra": 35000,
        "Spinach": 20000,
        "Molokhia": 22000,
        "Zucchini": 30000,
        "Broccoli": 35000,
        "Cauliflower": 30000,
        "Green Beans": 35000,
        "Peanuts": 30000,
        "Sesame": 32000,
        "Sunflower": 28000,
        "Sugar Cane": 25000,
        "Sugar Beet": 23000,
        "Orange": 25000,
        "Mandarin": 25000,
        "Lemon": 30000,
        "Mango": 40000,
        "Banana": 30000,
        "Grapes": 35000,
        "Strawberry": 45000,
        "Guava": 30000,
        "Peach": 35000,
        "Apricot": 40000,
        "Plum": 35000,
        "Apple": 40000,
        "Pear": 38000,
        "Pomegranate": 30000,
        "Watermelon": 18000,
        "Melon": 22000,
        "Fig": 30000,
        "Date": 35000,
        "Olive": 30000,
        "Other": 0
    }

    for crop, price in defaults.items():
        cur.execute("""
            INSERT OR IGNORE INTO crop_prices
            (crop, price, updated_at)
            VALUES (?, ?, ?)
        """, (
            crop,
            price,
            now()
        ))

    conn.commit()
    conn.close()


# ============================================================
# BASIC WIDGETS
# ============================================================

class GreenBackground(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*WHITE)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self._update,
            size=self._update
        )

    def _update(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size


class LargeButton(Button):

    def __init__(self, **kwargs):

        kwargs.setdefault("font_size", dp(18))
        kwargs.setdefault("height", dp(64))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_color", GREEN)

        # White text on green button.
        kwargs.setdefault("color", WHITE)

        super().__init__(**kwargs)


class BackButton(LargeButton):

    def __init__(self, **kwargs):

        kwargs["text"] = "BACK"
        kwargs["background_color"] = DARK_GREEN

        super().__init__(**kwargs)


class FieldLabel(Label):

    def __init__(self, **kwargs):

        kwargs.setdefault("color", BLACK)
        kwargs.setdefault("font_size", dp(16))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(32))
        kwargs.setdefault("halign", "left")
        kwargs.setdefault("valign", "middle")

        super().__init__(**kwargs)


class BigInput(TextInput):

    def __init__(self, **kwargs):

        kwargs.setdefault("font_size", dp(18))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(54))
        kwargs.setdefault("multiline", False)
        kwargs.setdefault("background_color", WHITE)
        kwargs.setdefault("foreground_color", BLACK)
        kwargs.setdefault("cursor_color", BLUE)

        super().__init__(**kwargs)


class BigSpinner(Spinner):

    def __init__(self, **kwargs):

        kwargs.setdefault("font_size", dp(18))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(54))
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_color", WHITE)
        kwargs.setdefault("color", BLACK)

        super().__init__(**kwargs)


# ============================================================
# MESSAGE POPUP
# ============================================================

def show_message(title, message, message_type="info"):

    if message_type == "success":
        text_color = GREEN
    elif message_type == "error":
        text_color = RED
    else:
        text_color = BLUE

    content = BoxLayout(
        orientation="vertical",
        padding=dp(18),
        spacing=dp(14)
    )

    label = Label(
        text=str(message),
        color=text_color,
        font_size=dp(18),
        bold=True,
        halign="center",
        valign="middle"
    )

    close_btn = LargeButton(
        text="OK",
        height=dp(58)
    )

    content.add_widget(label)
    content.add_widget(close_btn)

    popup = Popup(
        title=title,
        content=content,
        size_hint=(0.92, 0.55),
        background_color=WHITE,
        separator_color=GREEN,
        title_color=BLACK,
        title_size=dp(20),
        auto_dismiss=False
    )

    close_btn.bind(
        on_release=popup.dismiss
    )

    popup.open()


# ============================================================
# SCREEN BASE
# ============================================================

class BaseScreen(Screen):

    def title_label(self, text):

        return Label(
            text=text,
            color=GREEN,
            font_size=dp(25),
            bold=True,
            size_hint_y=None,
            height=dp(60),
            halign="center",
            valign="middle"
        )

    def add_field(
        self,
        box,
        label_text,
        default=""
    ):

        box.add_widget(
            FieldLabel(text=label_text)
        )

        inp = BigInput(text=default)

        box.add_widget(inp)

        return inp

    def add_crop_spinner(
        self,
        box,
        label_text="Crop"
    ):

        box.add_widget(
            FieldLabel(text=label_text)
        )

        spinner = BigSpinner(
            text=CROPS[0],
            values=CROPS
        )

        box.add_widget(spinner)

        return spinner

    def add_back(self, box):

        btn = BackButton()

        box.add_widget(btn)

        btn.bind(
            on_release=lambda *_:
            setattr(
                self.manager,
                "current",
                "home"
            )
        )


# ============================================================
# HOME
# ============================================================

class HomeScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10)
        )

        root.add_widget(
            self.title_label(
                "WASEET AL-KHAIR"
            )
        )

        subtitle = Label(
            text="Agricultural Trade & Banking Platform",
            color=BLUE,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(38)
        )

        root.add_widget(subtitle)

        scroll = ScrollView()

        menu = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(4),
            size_hint_y=None
        )

        menu.bind(
            minimum_height=menu.setter("height")
        )

        buttons = [
            ("FARMER REGISTRATION", "farmer_register"),
            ("FARMER ORDER", "farmer_order"),
            ("TRADER REGISTRATION", "trader_register"),
            ("PAYMENT", "payment"),
            ("BANK INCENTIVE", "bank"),
            ("SEARCH", "search"),
            ("TODAY'S CROP PRICES", "prices"),
            ("ABOUT / DEVELOPER", "about")
        ]

        for text, screen_name in buttons:

            btn = LargeButton(text=text)

            menu.add_widget(btn)

            btn.bind(
                on_release=lambda _, s=screen_name:
                setattr(
                    self.manager,
                    "current",
                    s
                )
            )

        scroll.add_widget(menu)

        root.add_widget(scroll)

        footer = Label(
            text="Program Developer: Adel Omar Abdel Aziz",
            color=BLUE,
            font_size=dp(13),
            size_hint_y=None,
            height=dp(38),
            halign="center"
        )

        root.add_widget(footer)

        self.add_widget(root)


# ============================================================
# FARMER REGISTRATION
# ============================================================

class FarmerRegisterScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label(
                "FARMER REGISTRATION"
            )
        )

        scroll = ScrollView()

        form = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None,
            padding=dp(5)
        )

        form.bind(
            minimum_height=form.setter("height")
        )

        # IMPORTANT:
        # Do NOT use self.name here because Screen.name
        # is reserved by Kivy.
        self.farmer_name_input = self.add_field(
            form,
            "Farmer Name"
        )

        self.farmer_mobile_input = self.add_field(
            form,
            "Mobile"
        )

        self.farmer_village_input = self.add_field(
            form,
            "Village / Area"
        )

        self.farmer_area_input = self.add_field(
            form,
            "Area - Feddan"
        )

        self.farmer_crop_spinner = self.add_crop_spinner(
            form,
            "Main Crop"
        )

        self.farmer_quantity_input = self.add_field(
            form,
            "Quantity - Ton"
        )

        self.farmer_price_input = self.add_field(
            form,
            "Price per Ton"
        )

        self.farmer_account_input = self.add_field(
            form,
            "Farmer Account Number"
        )

        save = LargeButton(
            text="SAVE FARMER"
        )

        form.add_widget(save)

        save.bind(
            on_release=self.save_farmer
        )

        self.add_back(form)

        scroll.add_widget(form)

        root.add_widget(scroll)

        self.add_widget(root)

    def save_farmer(self, *_):

        name = self.farmer_name_input.text.strip()

        if not name:

            show_message(
                "FARMER REGISTRATION",
                "Please enter the farmer name.",
                "error"
            )

            return

        try:

            area = float(
                self.farmer_area_input.text or 0
            )

            quantity = float(
                self.farmer_quantity_input.text or 0
            )

            price = float(
                self.farmer_price_input.text or 0
            )

        except ValueError:

            show_message(
                "FARMER REGISTRATION",
                "Area, quantity and price must be numbers.",
                "error"
            )

            return

        try:

            conn = get_connection()

            cur = conn.cursor()

            cur.execute("""
                INSERT INTO farmers
                (
                    name,
                    mobile,
                    village,
                    area,
                    crop,
                    quantity,
                    price_per_ton,
                    account,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                self.farmer_mobile_input.text.strip(),
                self.farmer_village_input.text.strip(),
                area,
                self.farmer_crop_spinner.text,
                quantity,
                price,
                self.farmer_account_input.text.strip(),
                now()
            ))

            farmer_id = cur.lastrowid

            conn.commit()
            conn.close()

        except Exception as e:

            show_message(
                "DATABASE ERROR",
                f"Could not save farmer.\n\n{e}",
                "error"
            )

            return

        show_message(
            "SUCCESS",
            f"Farmer saved successfully.\n\n"
            f"Farmer ID: {farmer_id}\n"
            f"Name: {name}\n"
            f"Account: "
            f"{self.farmer_account_input.text.strip() or 'Not entered'}",
            "success"
        )


# ============================================================
# FARMER ORDER
# ============================================================

class FarmerOrderScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label("FARMER ORDER")
        )

        scroll = ScrollView()

        form = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None,
            padding=dp(5)
        )

        form.bind(
            minimum_height=form.setter("height")
        )

        form.add_widget(
            FieldLabel(text="Select Farmer")
        )

        self.farmer_spinner = BigSpinner(
            text="Select Farmer",
            values=[]
        )

        form.add_widget(
            self.farmer_spinner
        )

        self.farmer_name = self.add_field(
            form,
            "Farmer Name"
        )

        self.crop = self.add_crop_spinner(
            form,
            "Crop"
        )

        self.quantity = self.add_field(
            form,
            "Quantity - Ton"
        )

        self.price = self.add_field(
            form,
            "Price per Ton"
        )

        self.account = self.add_field(
            form,
            "Farmer Account Number"
        )

        self.total_label = Label(
            text="Order Total: 0.00 EGP",
            color=BLUE,
            font_size=dp(20),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )

        form.add_widget(
            self.total_label
        )

        self.farmer_spinner.bind(
            text=self.select_farmer
        )

        self.quantity.bind(
            text=self.update_total
        )

        self.price.bind(
            text=self.update_total
        )

        send = LargeButton(
            text="SEND ORDER TO TRADER"
        )

        form.add_widget(send)

        send.bind(
            on_release=self.send_order
        )

        self.add_back(form)

        scroll.add_widget(form)

        root.add_widget(scroll)

        self.add_widget(root)

        self.load_farmers()

    def load_farmers(self):

        conn = get_connection()

        rows = conn.execute("""
            SELECT
                id,
                name,
                mobile,
                account,
                crop,
                quantity,
                price_per_ton
            FROM farmers
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        self.farmer_data = {
            f"{row['id']} - {row['name']}": row
            for row in rows
        }

        values = list(
            self.farmer_data.keys()
        )

        if values:

            self.farmer_spinner.values = values

            self.farmer_spinner.text = values[0]

            self.select_farmer(
                self.farmer_spinner,
                values[0]
            )

        else:

            self.farmer_spinner.values = [
                "No Farmers"
            ]

            self.farmer_spinner.text = "No Farmers"

    def select_farmer(
        self,
        spinner,
        text
    ):

        row = self.farmer_data.get(text)

        if not row:
            return

        self.farmer_name.text = (
            row["name"] or ""
        )

        self.account.text = (
            row["account"] or ""
        )

        if row["crop"]:
            self.crop.text = row["crop"]

        if row["quantity"]:
            self.quantity.text = str(
                row["quantity"]
            )

        if row["price_per_ton"]:
            self.price.text = str(
                row["price_per_ton"]
            )

        self.update_total()

    def update_total(self, *_):

        try:

            quantity = float(
                self.quantity.text or 0
            )

            price = float(
                self.price.text or 0
            )

            total = quantity * price

            self.total_label.text = (
                f"Order Total: "
                f"{total:,.2f} EGP"
            )

        except Exception:

            self.total_label.text = (
                "Order Total: 0.00 EGP"
            )

    def send_order(self, *_):

        if self.farmer_spinner.text in (
            "Select Farmer",
            "No Farmers"
        ):

            show_message(
                "FARMER ORDER",
                "Please select a farmer first.",
                "error"
            )

            return

        try:

            quantity = float(
                self.quantity.text
            )

            price = float(
                self.price.text
            )

        except ValueError:

            show_message(
                "FARMER ORDER",
                "Quantity and price must be numbers.",
                "error"
            )

            return

        if quantity <= 0 or price <= 0:

            show_message(
                "FARMER ORDER",
                "Quantity and price must be greater than zero.",
                "error"
            )

            return

        farmer_row = self.farmer_data.get(
            self.farmer_spinner.text
        )

        if not farmer_row:

            show_message(
                "FARMER ORDER",
                "Farmer data was not found.",
                "error"
            )

            return

        total = quantity * price

        try:

            conn = get_connection()

            cur = conn.cursor()

            cur.execute("""
                INSERT INTO orders
                (
                    farmer_id,
                    farmer_name,
                    farmer_mobile,
                    farmer_account,
                    trader_id,
                    trader_name,
                    crop,
                    quantity,
                    price_per_ton,
                    total_value,
                    status,
                    paid_amount,
                    created_at
                )
                VALUES
                (
                    ?, ?, ?, ?,
                    NULL, '',
                    ?, ?, ?, ?,
                    'SENT',
                    0,
                    ?
                )
            """, (
                farmer_row["id"],
                farmer_row["name"],
                farmer_row["mobile"],
                self.account.text.strip(),
                self.crop.text,
                quantity,
                price,
                total,
                now()
            ))

            order_id = cur.lastrowid

            conn.commit()
            conn.close()

        except Exception as e:

            show_message(
                "ORDER ERROR",
                f"Could not save order.\n\n{e}",
                "error"
            )

            return

        show_message(
            "ORDER SENT",
            f"Order sent successfully.\n\n"
            f"Order ID: {order_id}\n"
            f"Farmer: {farmer_row['name']}\n"
            f"Crop: {self.crop.text}\n"
            f"Quantity: {quantity:,.2f} Ton\n"
            f"Price/Ton: {price:,.2f} EGP\n"
            f"Total: {total:,.2f} EGP\n"
            f"Farmer Account: "
            f"{self.account.text.strip() or 'Not entered'}",
            "success"
        )


# ============================================================
# TRADER REGISTRATION
# ============================================================

class TraderRegisterScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label(
                "TRADER REGISTRATION"
            )
        )

        scroll = ScrollView()

        form = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None,
            padding=dp(5)
        )

        form.bind(
            minimum_height=form.setter("height")
        )

        # IMPORTANT:
        # Do NOT use self.name because Screen.name
        # is reserved by Kivy.
        self.trader_name_input = self.add_field(
            form,
            "Trader Name"
        )

        self.trader_village_input = self.add_field(
            form,
            "Village / Area"
        )

        self.trader_commercial_input = self.add_field(
            form,
            "Commercial Register - Optional"
        )

        self.trader_mobile_input = self.add_field(
            form,
            "Mobile"
        )

        self.trader_account_input = self.add_field(
            form,
            "Trader Account Number"
        )

        save = LargeButton(
            text="SAVE TRADER"
        )

        form.add_widget(save)

        save.bind(
            on_release=self.save_trader
        )

        self.add_back(form)

        scroll.add_widget(form)

        root.add_widget(scroll)

        self.add_widget(root)

    def save_trader(self, *_):

        name = self.trader_name_input.text.strip()

        if not name:

            show_message(
                "TRADER REGISTRATION",
                "Please enter the trader name.",
                "error"
            )

            return

        try:

            conn = get_connection()

            cur = conn.cursor()

            cur.execute("""
                INSERT INTO traders
                (
                    name,
                    village,
                    commercial_register,
                    mobile,
                    account,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                self.trader_village_input.text.strip(),
                self.trader_commercial_input.text.strip(),
                self.trader_mobile_input.text.strip(),
                self.trader_account_input.text.strip(),
                now()
            ))

            trader_id = cur.lastrowid

            conn.commit()
            conn.close()

        except Exception as e:

            show_message(
                "DATABASE ERROR",
                f"Could not save trader.\n\n{e}",
                "error"
            )

            return

        show_message(
            "SUCCESS",
            f"Trader saved successfully.\n\n"
            f"Trader ID: {trader_id}\n"
            f"Name: {name}\n"
            f"Account: "
            f"{self.trader_account_input.text.strip() or 'Not entered'}",
            "success"
        )


# ============================================================
# PAYMENT
# ============================================================

class PaymentScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label("PAYMENT")
        )

        scroll = ScrollView()

        form = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None,
            padding=dp(5)
        )

        form.bind(
            minimum_height=form.setter("height")
        )

        form.add_widget(
            FieldLabel(text="Select Trader")
        )

        self.trader_spinner = BigSpinner(
            text="Select Trader",
            values=[]
        )

        form.add_widget(
            self.trader_spinner
        )

        form.add_widget(
            FieldLabel(
                text="Select Incoming Order"
            )
        )

        self.order_spinner = BigSpinner(
            text="Select Order",
            values=[]
        )

        form.add_widget(
            self.order_spinner
        )

        self.trader_name = self.add_field(
            form,
            "Trader - Payer"
        )

        self.farmer_name = self.add_field(
            form,
            "Farmer - Receiver"
        )

        self.order_id = self.add_field(
            form,
            "Farmer Order ID"
        )

        self.farmer_account = self.add_field(
            form,
            "Farmer Account Number"
        )

        self.order_total = self.add_field(
            form,
            "Order Total"
        )

        self.already_paid = self.add_field(
            form,
            "Already Paid"
        )

        self.remaining = self.add_field(
            form,
            "Remaining Amount"
        )

        self.payment_amount = self.add_field(
            form,
            "Payment Amount"
        )

        self.fee_label = Label(
            text="Bank Fee: 0.00 EGP",
            color=RED,
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )

        form.add_widget(
            self.fee_label
        )

        self.net_label = Label(
            text="Net Payment: 0.00 EGP",
            color=BLUE,
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )

        form.add_widget(
            self.net_label
        )

        self.trader_spinner.bind(
            text=self.select_trader
        )

        self.order_spinner.bind(
            text=self.select_order
        )

        self.payment_amount.bind(
            text=self.calculate_payment
        )

        send = LargeButton(
            text="SEND PAYMENT"
        )

        form.add_widget(send)

        send.bind(
            on_release=self.send_payment
        )

        self.add_back(form)

        scroll.add_widget(form)

        root.add_widget(scroll)

        self.add_widget(root)

        self.load_traders()

    def load_traders(self):

        conn = get_connection()

        rows = conn.execute("""
            SELECT *
            FROM traders
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        self.trader_data = {
            f"{r['id']} - {r['name']}": r
            for r in rows
        }

        values = list(
            self.trader_data.keys()
        )

        if values:

            self.trader_spinner.values = values

            self.trader_spinner.text = values[0]

            self.select_trader(
                self.trader_spinner,
                values[0]
            )

        else:

            self.trader_spinner.values = [
                "No Traders"
            ]

            self.trader_spinner.text = "No Traders"

    def select_trader(
        self,
        spinner,
        text
    ):

        row = self.trader_data.get(text)

        if not row:
            return

        self.trader_name.text = (
            row["name"] or ""
        )

        self.load_orders()

    def load_orders(self):

        conn = get_connection()

        rows = conn.execute("""
            SELECT *
            FROM orders
            WHERE status IN
            (
                'SENT',
                'RECEIVED',
                'PARTIALLY PAID'
            )
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        self.order_data = {
            f"Order #{r['id']} - "
            f"{r['farmer_name']} - "
            f"{r['crop']}": r
            for r in rows
        }

        values = list(
            self.order_data.keys()
        )

        if values:

            self.order_spinner.values = values

            self.order_spinner.text = values[0]

            self.select_order(
                self.order_spinner,
                values[0]
            )

        else:

            self.order_spinner.values = [
                "No Incoming Orders"
            ]

            self.order_spinner.text = (
                "No Incoming Orders"
            )

    def select_order(
        self,
        spinner,
        text
    ):

        row = self.order_data.get(text)

        if not row:
            return

        self.farmer_name.text = (
            row["farmer_name"] or ""
        )

        self.order_id.text = str(
            row["id"]
        )

        self.farmer_account.text = (
            row["farmer_account"] or ""
        )

        total = float(
            row["total_value"] or 0
        )

        paid = float(
            row["paid_amount"] or 0
        )

        remaining = max(
            total - paid,
            0
        )

        self.order_total.text = (
            f"{total:.2f}"
        )

        self.already_paid.text = (
            f"{paid:.2f}"
        )

        self.remaining.text = (
            f"{remaining:.2f}"
        )

        self.payment_amount.text = ""

    def calculate_payment(self, *_):

        try:

            amount = float(
                self.payment_amount.text or 0
            )

        except ValueError:

            amount = 0

        fee = amount * BANK_FEE_RATE
        net = amount - fee

        self.fee_label.text = (
            f"Bank Fee: {fee:,.2f} EGP"
        )

        self.net_label.text = (
            f"Net Payment: {net:,.2f} EGP"
        )

    def send_payment(self, *_):

        if self.order_spinner.text in (
            "Select Order",
            "No Incoming Orders"
        ):

            show_message(
                "PAYMENT",
                "Please select an incoming order.",
                "error"
            )

            return

        trader = self.trader_data.get(
            self.trader_spinner.text
        )

        order = self.order_data.get(
            self.order_spinner.text
        )

        if not trader or not order:

            show_message(
                "PAYMENT",
                "Trader or order information was not found.",
                "error"
            )

            return

        try:

            amount = float(
                self.payment_amount.text
            )

        except ValueError:

            show_message(
                "PAYMENT",
                "Please enter a valid payment amount.",
                "error"
            )

            return

        if amount <= 0:

            show_message(
                "PAYMENT",
                "Payment must be greater than zero.",
                "error"
            )

            return

        total = float(
            order["total_value"] or 0
        )

        paid = float(
            order["paid_amount"] or 0
        )

        remaining = total - paid

        if amount > remaining:

            show_message(
                "PAYMENT",
                f"Payment is greater than the remaining amount.\n\n"
                f"Remaining: {remaining:,.2f} EGP",
                "error"
            )

            return

        fee = amount * BANK_FEE_RATE
        net = amount - fee
        new_paid = paid + amount

        if new_paid >= total:
            status = "PAID"
        elif new_paid > 0:
            status = "PARTIALLY PAID"
        else:
            status = "RECEIVED"

        try:

            conn = get_connection()

            cur = conn.cursor()

            cur.execute("""
                UPDATE orders
                SET
                    paid_amount = ?,
                    status = ?,
                    trader_id = ?,
                    trader_name = ?,
                    received_at = ?
                WHERE id = ?
            """, (
                new_paid,
                status,
                trader["id"],
                trader["name"],
                now(),
                order["id"]
            ))

            cur.execute("""
                INSERT INTO payments
                (
                    order_id,
                    trader_id,
                    trader_name,
                    farmer_id,
                    farmer_name,
                    farmer_account,
                    amount,
                    fee,
                    net_amount,
                    payment_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order["id"],
                trader["id"],
                trader["name"],
                order["farmer_id"],
                order["farmer_name"],
                order["farmer_account"],
                amount,
                fee,
                net,
                now()
            ))

            conn.commit()
            conn.close()

        except Exception as e:

            show_message(
                "PAYMENT ERROR",
                f"Could not record payment.\n\n{e}",
                "error"
            )

            return

        show_message(
            "PAYMENT SENT",
            f"Payment recorded successfully.\n\n"
            f"Trader: {trader['name']}\n"
            f"Farmer: {order['farmer_name']}\n"
            f"Order ID: {order['id']}\n"
            f"Farmer Account: "
            f"{order['farmer_account'] or 'Not entered'}\n"
            f"Payment: {amount:,.2f} EGP\n"
            f"Fee: {fee:,.2f} EGP\n"
            f"Net: {net:,.2f} EGP\n"
            f"Order Status: {status}",
            "success"
        )

        self.load_orders()


# ============================================================
# BANK INCENTIVE
# ============================================================

class BankScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label(
                "BANK INCENTIVE"
            )
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(5)
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # Clear bank incentive information.
        info = Label(
            text=(
                f"Bank Incentive\n"
                f"{BANK_INCENTIVE_PER_TON:,.2f} EGP "
                f"for each Ton"
            ),
            color=BLUE,
            font_size=dp(19),
            bold=True,
            size_hint_y=None,
            height=dp(80),
            halign="center",
            valign="middle"
        )

        content.add_widget(info)

        refresh = LargeButton(
            text="REFRESH BANK INCENTIVE"
        )

        content.add_widget(refresh)

        refresh.bind(
            on_release=lambda *_:
            self.load_data()
        )

        self.result = Label(
            text="Loading...",
            color=BLACK,
            font_size=dp(17),
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.result.bind(
            texture_size=lambda obj, size:
            setattr(
                obj,
                "height",
                size[1] + dp(20)
            )
        )

        content.add_widget(
            self.result
        )

        self.add_back(content)

        scroll.add_widget(content)

        root.add_widget(scroll)

        self.add_widget(root)

        self.load_data()

    def load_data(self):

        conn = get_connection()

        rows = conn.execute("""
            SELECT *
            FROM orders
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        if not rows:

            self.result.text = (
                "No orders found.\n\n"
                f"Bank incentive: "
                f"{BANK_INCENTIVE_PER_TON:,.2f} "
                f"EGP per Ton."
            )

            return

        lines = []

        for row in rows:

            quantity = float(
                row["quantity"] or 0
            )

            price = float(
                row["price_per_ton"] or 0
            )

            total = float(
                row["total_value"] or 0
            )

            incentive = (
                quantity *
                BANK_INCENTIVE_PER_TON
            )

            grand_total = (
                total +
                incentive
            )

            lines.append(
                f"ORDER ID: {row['id']}\n"
                f"Farmer: {row['farmer_name'] or ''}\n"
                f"Farmer Account: "
                f"{row['farmer_account'] or 'Not entered'}\n"
                f"Crop: {row['crop'] or ''}\n"
                f"Quantity: {quantity:,.2f} Ton\n"
                f"Price/Ton: {price:,.2f} EGP\n"
                f"Order Value: {total:,.2f} EGP\n"
                f"Bank Incentive: "
                f"{incentive:,.2f} EGP\n"
                f"Incentive Rate: "
                f"{BANK_INCENTIVE_PER_TON:,.2f} EGP/Ton\n"
                f"Total with Incentive: "
                f"{grand_total:,.2f} EGP\n"
                f"Order Status: {row['status']}\n"
                f"----------------------------------"
            )

        self.result.text = "\n\n".join(lines)


# ============================================================
# SEARCH
# ============================================================

class SearchScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label("SEARCH")
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
            padding=dp(5)
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        content.add_widget(
            FieldLabel(text="Search Type")
        )

        self.search_type = BigSpinner(
            text="Farmer",
            values=[
                "Farmer",
                "Trader"
            ]
        )

        content.add_widget(
            self.search_type
        )

        content.add_widget(
            FieldLabel(text="Search By")
        )

        self.search_by = BigSpinner(
            text="Name",
            values=[
                "Name",
                "Mobile",
                "Village / Area"
            ]
        )

        content.add_widget(
            self.search_by
        )

        self.search_text = self.add_field(
            content,
            "Search Text"
        )

        search = LargeButton(
            text="SEARCH"
        )

        content.add_widget(search)

        search.bind(
            on_release=self.perform_search
        )

        self.result = Label(
            text="Search results will appear here.",
            color=BLUE,
            font_size=dp(17),
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.result.bind(
            texture_size=lambda obj, size:
            setattr(
                obj,
                "height",
                size[1] + dp(20)
            )
        )

        content.add_widget(
            self.result
        )

        self.add_back(content)

        scroll.add_widget(content)

        root.add_widget(scroll)

        self.add_widget(root)

    def perform_search(self, *_):

        search_type = self.search_type.text
        search_by = self.search_by.text
        term = self.search_text.text.strip()

        if not term:

            show_message(
                "SEARCH",
                "Please enter search text.",
                "error"
            )

            return

        conn = get_connection()

        if search_type == "Farmer":

            table = "farmers"

            if search_by == "Name":

                query = """
                    SELECT *
                    FROM farmers
                    WHERE name LIKE ?
                    ORDER BY id DESC
                """

            elif search_by == "Mobile":

                query = """
                    SELECT *
                    FROM farmers
                    WHERE mobile LIKE ?
                    ORDER BY id DESC
                """

            else:

                query = """
                    SELECT *
                    FROM farmers
                    WHERE village LIKE ?
                    ORDER BY id DESC
                """

        else:

            table = "traders"

            if search_by == "Name":

                query = """
                    SELECT *
                    FROM traders
                    WHERE name LIKE ?
                    ORDER BY id DESC
                """

            elif search_by == "Mobile":

                query = """
                    SELECT *
                    FROM traders
                    WHERE mobile LIKE ?
                    ORDER BY id DESC
                """

            else:

                query = """
                    SELECT *
                    FROM traders
                    WHERE village LIKE ?
                    ORDER BY id DESC
                """

        rows = conn.execute(
            query,
            (f"%{term}%",)
        ).fetchall()

        conn.close()

        if not rows:

            self.result.text = (
                f"No {table} records found."
            )

            return

        lines = []

        for row in rows:

            if search_type == "Farmer":

                lines.append(
                    f"Farmer ID: {row['id']}\n"
                    f"Name: {row['name']}\n"
                    f"Mobile: {row['mobile'] or ''}\n"
                    f"Village: {row['village'] or ''}\n"
                    f"Crop: {row['crop'] or ''}\n"
                    f"Account: {row['account'] or ''}\n"
                    f"----------------------------------"
                )

            else:

                lines.append(
                    f"Trader ID: {row['id']}\n"
                    f"Name: {row['name']}\n"
                    f"Mobile: {row['mobile'] or ''}\n"
                    f"Village: {row['village'] or ''}\n"
                    f"Commercial Register: "
                    f"{row['commercial_register'] or ''}\n"
                    f"Account: {row['account'] or ''}\n"
                    f"----------------------------------"
                )

        self.result.text = "\n\n".join(lines)


# ============================================================
# CROP PRICES
# ============================================================

class PricesScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(
            self.title_label(
                "TODAY'S CROP PRICES"
            )
        )

        info = Label(
            text="Local crop prices - Offline",
            color=BLUE,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            halign="center"
        )

        root.add_widget(info)

        scroll = ScrollView()

        table = GridLayout(
            cols=3,
            spacing=dp(2),
            padding=dp(3),
            size_hint_y=None
        )

        table.bind(
            minimum_height=table.setter("height")
        )

        # Header labels without invalid canvas_before usage.
        headers = [
            "CROP",
            "PRICE",
            "UPDATED"
        ]

        for header in headers:

            header_box = BoxLayout(
                size_hint_y=None,
                height=dp(45)
            )

            with header_box.canvas.before:

                Color(*GREEN)

                header_box.bg = RoundedRectangle(
                    pos=header_box.pos,
                    size=header_box.size
                )

            def update_header(
                widget,
                *_,
                bg=header_box.bg
            ):
                bg.pos = widget.pos
                bg.size = widget.size

            header_box.bind(
                pos=update_header,
                size=update_header
            )

            label = Label(
                text=header,
                color=WHITE,
                font_size=dp(15),
                bold=True
            )

            header_box.add_widget(label)

            table.add_widget(header_box)

        conn = get_connection()

        rows = conn.execute("""
            SELECT
                crop,
                price,
                updated_at
            FROM crop_prices
            ORDER BY id
        """).fetchall()

        conn.close()

        for row in rows:

            crop_label = Label(
                text=row["crop"],
                color=BLACK,
                font_size=dp(14),
                size_hint_y=None,
                height=dp(42)
            )

            price_label = Label(
                text=f"{float(row['price'] or 0):,.2f}",
                color=BLUE,
                font_size=dp(14),
                size_hint_y=None,
                height=dp(42)
            )

            date_label = Label(
                text=row["updated_at"] or "",
                color=BLACK,
                font_size=dp(11),
                size_hint_y=None,
                height=dp(42)
            )

            table.add_widget(crop_label)
            table.add_widget(price_label)
            table.add_widget(date_label)

        scroll.add_widget(table)

        root.add_widget(scroll)

        refresh = LargeButton(
            text="REFRESH LOCAL PRICE TABLE"
        )

        root.add_widget(refresh)

        refresh.bind(
            on_release=self.refresh_prices
        )

        back = BackButton()

        root.add_widget(back)

        back.bind(
            on_release=lambda *_:
            setattr(
                self.manager,
                "current",
                "home"
            )
        )

        self.add_widget(root)

    def refresh_prices(self, *_):

        show_message(
            "CROP PRICES",
            "The local crop price table is available offline.",
            "info"
        )


# ============================================================
# ABOUT
# ============================================================

class AboutScreen(BaseScreen):

    def on_enter(self):

        self.clear_widgets()

        root = GreenBackground(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12)
        )

        root.add_widget(
            self.title_label(
                "ABOUT / DEVELOPER"
            )
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            padding=dp(10)
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        logo = Label(
            text="WASEET\nAL-KHAIR",
            color=GREEN,
            font_size=dp(32),
            bold=True,
            size_hint_y=None,
            height=dp(110),
            halign="center"
        )

        content.add_widget(logo)

        information = Label(
            text=(
                "Agricultural Trade & Banking Platform\n\n"
                "Program Developer\n"
                "Adel Omar Abdel Aziz\n\n"
                "Android Ready\n"
                "Offline First\n"
                "SQLite Database\n\n"
                "WASEET AL-KHAIR"
            ),
            color=BLACK,
            font_size=dp(18),
            halign="center",
            valign="top",
            size_hint_y=None,
            height=dp(270)
        )

        content.add_widget(
            information
        )

        self.add_back(content)

        scroll.add_widget(content)

        root.add_widget(scroll)

        self.add_widget(root)


# ============================================================
# APP
# ============================================================

class WaseetAlKhairApp(App):

    title = APP_NAME

    def build(self):

        Window.clearcolor = WHITE

        init_database()

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(
                name="home"
            )
        )

        manager.add_widget(
            FarmerRegisterScreen(
                name="farmer_register"
            )
        )

        manager.add_widget(
            FarmerOrderScreen(
                name="farmer_order"
            )
        )

        manager.add_widget(
            TraderRegisterScreen(
                name="trader_register"
            )
        )

        manager.add_widget(
            PaymentScreen(
                name="payment"
            )
        )

        manager.add_widget(
            BankScreen(
                name="bank"
            )
        )

        manager.add_widget(
            SearchScreen(
                name="search"
            )
        )

        manager.add_widget(
            PricesScreen(
                name="prices"
            )
        )

        manager.add_widget(
            AboutScreen(
                name="about"
            )
        )

        return manager


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    WaseetAlKhairApp().run()
