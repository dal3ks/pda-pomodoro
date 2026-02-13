import tkinter as tk
from tkinter import ttk, font, messagebox
import json
import os
import random
import winsound
from datetime import datetime

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Dreamy Timer ✨")
        self.root.geometry("450x680")
        
        # Load custom font and sound
        self.load_custom_resources()
        
        # Load settings
        self.settings_file = "pomodoro_settings.json"
        self.load_settings()
        
        # Apply current theme
        self.apply_theme()
        
        # Timer settings (load from settings)
        self.work_time = self.settings.get("work_minutes", 25) * 60
        self.break_time = self.settings.get("break_minutes", 5) * 60
        self.time_left = self.work_time
        self.is_running = False
        self.is_work_session = True
        self.current_goal = ""
        self.session_count = 0
        
        # PDA-friendly messages (expanded)
        self.start_messages = [
            "you're doing great",
            "take your time",
            "no pressure, just vibes",
            "one step at a time",
            "you've got this if you want"
        ]
        self.break_messages = [
            "it's okay to pause",
            "you're allowed to rest",
            "breathe and reset 💜",
            "gentle break time",
            "rest is productive too"
        ]
        self.end_messages = [
            "working at your own pace",
            "being here is enough",
            "you did well ✨",
            "that was great!",
            "proud of you 💜"
        ]
        
        # Center the window on screen
        self.center_window()
        
        # Crate background canvas FIRST
        self.create_background()
        
        # Create main UI
        self.create_widgets()
        
        # Mini window (initially hidden)
        self.mini_window = None
        
        # Show start message
        self.show_message(random.choice(self.start_messages))
    
    def load_custom_resources(self):
        """Load custom font and sound files"""
        import os
        import sys
        from tkinter import font as tkfont
        
        # Get the directory where the script/exe is running
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            application_path = sys._MEIPASS
        else:
            # Running as script
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        # Load custom font
        self.minecraft_font_path = os.path.join(application_path, "Minecraft.ttf")
        self.custom_font_loaded = False
        
        try:
            # Try to load the font
            if os.path.exists(self.minecraft_font_path):
                # For Windows, we need to use pyglet or register the font
                # Simple approach: just reference it by path
                self.pixel_font = ("Minecraft", 56, "bold")
                self.custom_font_loaded = True
            else:
                # Fallback to Courier New
                self.pixel_font = ("Courier New", 56, "bold")
        except:
            # Fallback to Courier New
            self.pixel_font = ("Courier New", 56, "bold")
        
        # Load sound file
        self.sound_path = os.path.join(application_path, "Bomberman_93_Password.mp3")
        
    def load_settings(self):
        """Load settings from JSON file"""
        default_settings = {
            "saved_goals": [],
            "current_theme": "purple",
            "sound_enabled": True,
            "mini_window_position": None,
            "total_sessions_today": 0,
            "last_session_date": "",
            "work_minutes": 25,
            "break_minutes": 5
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
                # Reset session count if it's a new day
                today = datetime.now().strftime("%Y-%m-%d")
                if self.settings.get("last_session_date") != today:
                    self.settings["total_sessions_today"] = 0
                    self.settings["last_session_date"] = today
                # Add work/break minutes if not present (for backwards compatibility)
                if "work_minutes" not in self.settings:
                    self.settings["work_minutes"] = 25
                if "break_minutes" not in self.settings:
                    self.settings["break_minutes"] = 5
            else:
                self.settings = default_settings
        except:
            self.settings = default_settings
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def apply_theme(self):
        """Apply color theme"""
        themes = {
            "purple": {
                "bg": "#e6dcf5",
                "primary": "#6b5b95",
                "secondary": "#8e7cc3",
                "accent1": "#c8b6e2",
                "accent2": "#d4c5f0",
                "accent3": "#b19cd9",
                "gradient_top": "#efe9ff",
                "gradient_bottom": "#d6d0f5"
            },
            "pink": {
                "bg": "#fce4ec",
                "primary": "#c2185b",
                "secondary": "#e91e63",
                "accent1": "#f8bbd0",
                "accent2": "#f48fb1",
                "accent3": "#f06292",
                "gradient_top": "#fff0f5",
                "gradient_bottom": "#fce4ec"
            },
            "blue": {
                "bg": "#e3f2fd",
                "primary": "#1565c0",
                "secondary": "#1976d2",
                "accent1": "#90caf9",
                "accent2": "#64b5f6",
                "accent3": "#42a5f5",
                "gradient_top": "#f0f8ff",
                "gradient_bottom": "#e3f2fd"
            },
            "mint": {
                "bg": "#e0f2f1",
                "primary": "#00695c",
                "secondary": "#00897b",
                "accent1": "#80cbc4",
                "accent2": "#4db6ac",
                "accent3": "#26a69a",
                "gradient_top": "#f0fff4",
                "gradient_bottom": "#e0f2f1"
            },
            "peach": {
                "bg": "#fff3e0",
                "primary": "#e65100",
                "secondary": "#f57c00",
                "accent1": "#ffcc80",
                "accent2": "#ffb74d",
                "accent3": "#ffa726",
                "gradient_top": "#fffaf0",
                "gradient_bottom": "#fff3e0"
            }
        }
        
        theme_name = self.settings.get("current_theme", "purple")
        self.theme = themes.get(theme_name, themes["purple"])
        self.root.configure(bg=self.theme["bg"])
        
    def center_window(self):
        self.root.update_idletasks()
        width = 450
        height = 680  # Increased from 650 to 680 for better button spacing
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_background(self):
        """Simple dreamy gradient background with moon and sparkles"""
        self.bg_canvas = tk.Canvas(self.root, width=450, height=680, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)

        # Gradient colours (top -> bottom)
        top_color = self.theme.get("gradient_top", "#efe9ff")  # soft lavender
        bottom_color = self.theme.get("gradient_bottom", "#d6d0f5")  # dusk purple

        self._draw_vertical_gradient(self.bg_canvas, 450, 680, top_color, bottom_color)

        # Moon
        self.bg_canvas.create_oval(300, 40, 360, 100, fill="#fff8dc", outline="")

        # Sparkles
        for x, y in [(80, 120), (120, 90), (200, 140), (350, 180)]:
            self.bg_canvas.create_oval(x, y, x+4, y+4, fill="#ffd700", outline="")
        
        # Add some extra tiny stars
        for x, y in [(50, 200), (400, 150), (100, 500), (380, 450), (150, 350)]:
            self.bg_canvas.create_oval(x, y, x+2, y+2, fill="#ffffff", outline="")
    
    def _draw_vertical_gradient(self, canvas, width, height, start, end):
        """Helper to draw vertical gradient"""
        r1, g1, b1 = canvas.winfo_rgb(start)
        r2, g2, b2 = canvas.winfo_rgb(end)

        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            color = "#%04x%04x%04x" % (
                int(r1 + r_ratio * i),
                int(g1 + g_ratio * i),
                int(b1 + b_ratio * i)
            )
            canvas.create_line(0, i, width, i, fill=color)

        
    def create_widgets(self):
        # Make widgets use canvas as parent or use a transparent approach
        # We'll place widgets directly on the root and the canvas will be behind them
        
        # Top frame for settings
        top_frame = tk.Frame(self.root, bg=self.theme["gradient_top"], highlightthickness=0)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # Settings button (left)
        settings_btn = tk.Button(
            top_frame,
            text="⚙️ Settings",
            command=self.show_settings,
            bg=self.theme["accent2"],
            fg=self.theme["primary"],
            font=("Courier New", 9),
            relief="flat",
            cursor="hand2"
        )
        settings_btn.pack(side="left")
        
        # Minimize button (right)
        self.minimize_button = tk.Button(
            top_frame,
            text="➖ Minimize",
            command=self.create_mini_window,
            bg=self.theme["accent2"],
            fg=self.theme["primary"],
            font=("Courier New", 9),
            relief="flat",
            cursor="hand2"
        )
        self.minimize_button.pack(side="right", padx=5)
        
        # Session counter (right, before minimize)
        self.session_counter_label = tk.Label(
            top_frame,
            text=f"Sessions today: {self.settings.get('total_sessions_today', 0)}",
            font=("Courier New", 9),
            fg=self.theme["primary"],
            bg=self.theme["gradient_top"]
        )
        self.session_counter_label.pack(side="right", padx=10)
        
        # Title with sparkles
        title_frame = tk.Frame(self.root, bg=self.theme["gradient_top"])
        title_frame.pack(pady=10)
        
        self.title_label = tk.Label(
            title_frame,
            text="✨ Work Time ✨",
            font=("Courier New", 18, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["gradient_top"]
        )
        self.title_label.pack()
        
        # Message label (for PDA-friendly messages)
        self.message_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 10),
            fg=self.theme["secondary"],
            bg=self.theme["gradient_top"],
            wraplength=400
        )
        self.message_label.pack(pady=5)
        
        # Current goal label (above hourglass)
        self.goal_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 11, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"],
            wraplength=400,
            height=3
        )
        self.goal_label.pack(pady=10)
        
        # Hourglass canvas
        self.hourglass_canvas = tk.Canvas(
            self.root,
            width=200,
            height=220,
            bg=self.theme["bg"],
            highlightthickness=0
        )
        self.hourglass_canvas.pack(pady=10)
        self.draw_hourglass()
        
        # Timer display (pixel style font)
        self.timer_label = tk.Label(
            self.root,
            text="25:00",
            font=self.pixel_font,
            fg=self.theme["primary"],
            bg=self.theme["gradient_bottom"]
        )
        self.timer_label.pack(pady=15)
        
        # Buttons with dreamy colors
        button_frame = tk.Frame(self.root, bg=self.theme["gradient_bottom"])
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            bg=self.theme["accent1"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            width=8,
            height=1,
            relief="flat",
            cursor="hand2"
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            command=self.pause_timer,
            bg=self.theme["accent2"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            width=8,
            height=1,
            relief="flat",
            cursor="hand2"
        )
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            bg=self.theme["accent3"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            width=8,
            height=1,
            relief="flat",
            cursor="hand2"
        )
        self.reset_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Background canvas is already behind because we created it first with .place()
        # and all other widgets use .pack() which layers on top
        
    def draw_hourglass(self):
        """Draw the dreamy sparkly hourglass"""
        c = self.hourglass_canvas
        c.delete("all")
        
        # Use theme colors
        rim_color = self.theme["accent3"]
        glass_color = self.theme["accent1"]
        sand_color = self.theme["accent2"]
        
        # Scale factor for pixel art
        scale = 8
        base_x = 50
        base_y = 10
        
        # Draw sparkles
        sparkle_coords = [
            (1, 3), (0, 4), (2, 4),  # top left
            (18, 5), (19, 6),  # top right
            (2, 15), (1, 16),  # bottom left
            (17, 14), (18, 15)  # bottom right
        ]
        for x, y in sparkle_coords:
            c.create_rectangle(
                base_x + x*scale, base_y + y*scale,
                base_x + x*scale + scale, base_y + y*scale + scale,
                fill="#ffd700", outline=""
            )
        
        # Top rim
        self.draw_pixels(c, base_x, base_y, [(5,2), (6,2), (7,2), (8,2), (9,2), (10,2), (11,2), (12,2), (13,2), (14,2)], rim_color, scale)
        self.draw_pixels(c, base_x, base_y, [(4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (10,3), (11,3), (12,3), (13,3), (14,3), (15,3)], rim_color, scale)
        
        # Glass outline top
        self.draw_pixels(c, base_x, base_y, [(6,4), (7,4), (8,4), (9,4), (10,4), (11,4), (12,4), (13,4)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(7,5), (8,5), (9,5), (10,5), (11,5), (12,5)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(8,6), (9,6), (10,6), (11,6)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(9,7), (10,7)], self.theme["secondary"], scale)
        
        # Sand in top
        self.draw_pixels(c, base_x, base_y, [(7,5), (8,5), (9,5), (10,5), (11,5), (12,5)], glass_color, scale)
        self.draw_pixels(c, base_x, base_y, [(8,6), (9,6), (10,6), (11,6)], sand_color, scale)
        
        # Middle
        self.draw_pixels(c, base_x, base_y, [(9,8), (10,8), (9,9), (10,9)], self.theme["bg"], scale)
        
        # Glass outline bottom
        self.draw_pixels(c, base_x, base_y, [(9,10), (10,10)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(8,11), (9,11), (10,11), (11,11)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(7,12), (8,12), (9,12), (10,12), (11,12), (12,12)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(6,13), (7,13), (8,13), (9,13), (10,13), (11,13), (12,13), (13,13)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(6,14), (7,14), (8,14), (9,14), (10,14), (11,14), (12,14), (13,14)], self.theme["secondary"], scale)
        self.draw_pixels(c, base_x, base_y, [(6,15), (7,15), (8,15), (9,15), (10,15), (11,15), (12,15), (13,15)], self.theme["secondary"], scale)
        
        # Sand in bottom
        self.draw_pixels(c, base_x, base_y, [(8,14), (9,14), (10,14), (11,14)], glass_color, scale)
        self.draw_pixels(c, base_x, base_y, [(8,15), (9,15), (10,15), (11,15)], glass_color, scale)
        
        # Bottom rim
        self.draw_pixels(c, base_x, base_y, [(4,16), (5,16), (6,16), (7,16), (8,16), (9,16), (10,16), (11,16), (12,16), (13,16), (14,16), (15,16)], rim_color, scale)
        self.draw_pixels(c, base_x, base_y, [(5,17), (6,17), (7,17), (8,17), (9,17), (10,17), (11,17), (12,17), (13,17), (14,17)], rim_color, scale)
        
    def draw_pixels(self, canvas, base_x, base_y, coords, color, scale):
        """Helper to draw pixel blocks"""
        for x, y in coords:
            canvas.create_rectangle(
                base_x + x*scale, base_y + y*scale,
                base_x + x*scale + scale, base_y + y*scale + scale,
                fill=color, outline=""
            )
    
    def show_settings(self):
        """Show settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("400x650")
        settings_window.configure(bg=self.theme["bg"])
        
        # Center settings window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - 200
        y = (settings_window.winfo_screenheight() // 2) - 325
        settings_window.geometry(f'400x650+{x}+{y}')
        
        # Title
        title = tk.Label(
            settings_window,
            text="⚙️ Settings ⚙️",
            font=("Courier New", 16, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        title.pack(pady=15)
        
        # Theme selection
        theme_frame = tk.LabelFrame(
            settings_window,
            text="Color Theme",
            font=("Courier New", 11, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        theme_frame.pack(pady=10, padx=20, fill="x")
        
        themes = ["purple", "pink", "blue", "mint", "peach"]
        for theme in themes:
            btn = tk.Button(
                theme_frame,
                text=theme.capitalize(),
                command=lambda t=theme: self.change_theme(t, settings_window),
                bg=self.theme["accent1"],
                fg=self.theme["primary"],
                font=("Courier New", 10),
                relief="flat",
                cursor="hand2",
                width=12
            )
            btn.pack(pady=3)
        
        # Sound toggle
        sound_frame = tk.LabelFrame(
            settings_window,
            text="Sound",
            font=("Courier New", 11, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        sound_frame.pack(pady=10, padx=20, fill="x")
        
        self.sound_var = tk.BooleanVar(value=self.settings.get("sound_enabled", True))
        sound_check = tk.Checkbutton(
            sound_frame,
            text="Enable notification sound",
            variable=self.sound_var,
            command=self.toggle_sound,
            font=("Courier New", 10),
            fg=self.theme["primary"],
            bg=self.theme["bg"],
            selectcolor=self.theme["accent1"]
        )
        sound_check.pack(pady=5)
        
        # Timer Duration Settings
        duration_frame = tk.LabelFrame(
            settings_window,
            text="Timer Duration (minutes)",
            font=("Courier New", 11, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        duration_frame.pack(pady=10, padx=20, fill="x")
        
        # Work duration
        work_duration_frame = tk.Frame(duration_frame, bg=self.theme["bg"])
        work_duration_frame.pack(pady=5, padx=10, fill="x")
        
        tk.Label(
            work_duration_frame,
            text="Work session:",
            font=("Courier New", 10),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        ).pack(side="left", padx=5)
        
        self.work_minutes_var = tk.StringVar(value=str(self.settings.get("work_minutes", 25)))
        work_entry = tk.Entry(
            work_duration_frame,
            textvariable=self.work_minutes_var,
            font=("Courier New", 10),
            width=5,
            bg=self.theme["bg"],
            fg=self.theme["primary"]
        )
        work_entry.pack(side="left", padx=5)
        
        tk.Label(
            work_duration_frame,
            text="minutes",
            font=("Courier New", 10),
            fg=self.theme["secondary"],
            bg=self.theme["bg"]
        ).pack(side="left", padx=5)
        
        # Break duration
        break_duration_frame = tk.Frame(duration_frame, bg=self.theme["bg"])
        break_duration_frame.pack(pady=5, padx=10, fill="x")
        
        tk.Label(
            break_duration_frame,
            text="Break session:",
            font=("Courier New", 10),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        ).pack(side="left", padx=5)
        
        self.break_minutes_var = tk.StringVar(value=str(self.settings.get("break_minutes", 5)))
        break_entry = tk.Entry(
            break_duration_frame,
            textvariable=self.break_minutes_var,
            font=("Courier New", 10),
            width=5,
            bg=self.theme["bg"],
            fg=self.theme["primary"]
        )
        break_entry.pack(side="left", padx=5)
        
        tk.Label(
            break_duration_frame,
            text="minutes",
            font=("Courier New", 10),
            fg=self.theme["secondary"],
            bg=self.theme["bg"]
        ).pack(side="left", padx=5)
        
        # Save duration button
        save_duration_btn = tk.Button(
            duration_frame,
            text="Save Timer Settings",
            command=self.save_timer_duration,
            bg=self.theme["accent1"],
            fg=self.theme["primary"],
            font=("Courier New", 9),
            relief="flat",
            cursor="hand2"
        )
        save_duration_btn.pack(pady=8)
        
        # Saved goals management
        goals_frame = tk.LabelFrame(
            settings_window,
            text="Saved Goals",
            font=("Courier New", 11, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        goals_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Listbox for saved goals
        goals_list = tk.Listbox(
            goals_frame,
            font=("Courier New", 9),
            bg=self.theme["bg"],
            fg=self.theme["primary"],
            selectbackground=self.theme["accent1"]
        )
        goals_list.pack(pady=5, padx=5, fill="both", expand=True)
        
        for goal in self.settings.get("saved_goals", []):
            goals_list.insert(tk.END, goal)
        
        delete_btn = tk.Button(
            goals_frame,
            text="Delete Selected Goal",
            command=lambda: self.delete_goal(goals_list),
            bg=self.theme["accent3"],
            fg=self.theme["primary"],
            font=("Courier New", 9),
            relief="flat",
            cursor="hand2"
        )
        delete_btn.pack(pady=5)
        
        # Close button
        close_btn = tk.Button(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            bg=self.theme["accent1"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        close_btn.pack(pady=15)
    
    def change_theme(self, theme_name, settings_window):
        """Change color theme"""
        self.settings["current_theme"] = theme_name
        self.save_settings()
        messagebox.showinfo("Theme Changed", f"Theme changed to {theme_name.capitalize()}!\nRestart the timer to see the full effect.")
        settings_window.destroy()
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.settings["sound_enabled"] = self.sound_var.get()
        self.save_settings()
    
    def save_timer_duration(self):
        """Save custom timer duration settings"""
        try:
            # Get and validate the values
            work_mins = int(self.work_minutes_var.get())
            break_mins = int(self.break_minutes_var.get())
            
            # Validate they're reasonable (between 1 and 120 minutes)
            if 1 <= work_mins <= 120 and 1 <= break_mins <= 120:
                # Save to settings
                self.settings["work_minutes"] = work_mins
                self.settings["break_minutes"] = break_mins
                self.save_settings()
                
                # Update the timer
                self.work_time = work_mins * 60
                self.break_time = break_mins * 60
                
                # Reset current timer to new duration
                if self.is_work_session:
                    self.time_left = self.work_time
                else:
                    self.time_left = self.break_time
                
                self.update_display()
                
                messagebox.showinfo("Timer Updated", f"Timer set to {work_mins} min work / {break_mins} min break!")
            else:
                messagebox.showwarning("Invalid Input", "Please enter values between 1 and 120 minutes")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers")
    
    def delete_goal(self, goals_list):
        """Delete selected goal from saved goals"""
        try:
            selection = goals_list.curselection()
            if selection:
                index = selection[0]
                goal = goals_list.get(index)
                self.settings["saved_goals"].remove(goal)
                self.save_settings()
                goals_list.delete(index)
                messagebox.showinfo("Deleted", f"Deleted: {goal}")
        except:
            messagebox.showwarning("No Selection", "Please select a goal to delete")
    
    def show_message(self, message):
        """Display a PDA-friendly message"""
        self.message_label.config(text=message)
        # Clear message after 4 seconds
        self.root.after(4000, lambda: self.message_label.config(text=""))
    
    def ask_for_goal(self):
        """Show popup to ask for session goal"""
        goal_window = tk.Toplevel(self.root)
        goal_window.title("✨ Set Your Intention ✨")
        goal_window.geometry("400x300")
        goal_window.configure(bg=self.theme["bg"])
        
        # Center window
        goal_window.update_idletasks()
        x = (goal_window.winfo_screenwidth() // 2) - 200
        y = (goal_window.winfo_screenheight() // 2) - 150
        goal_window.geometry(f'400x300+{x}+{y}')
        
        # Make it modal
        goal_window.transient(self.root)
        goal_window.grab_set()
        
        # Title
        title = tk.Label(
            goal_window,
            text="What's this session for?",
            font=("Courier New", 13, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        title.pack(pady=20)
        
        # Dropdown for saved goals
        saved_goals = self.settings.get("saved_goals", [])
        
        if saved_goals:
            dropdown_label = tk.Label(
                goal_window,
                text="Pick a recent goal:",
                font=("Courier New", 10),
                fg=self.theme["secondary"],
                bg=self.theme["bg"]
            )
            dropdown_label.pack(pady=5)
            
            goal_var = tk.StringVar()
            dropdown = ttk.Combobox(
                goal_window,
                textvariable=goal_var,
                values=saved_goals,
                font=("Courier New", 10),
                width=35
            )
            dropdown.pack(pady=5)
            
            or_label = tk.Label(
                goal_window,
                text="- or -",
                font=("Courier New", 10),
                fg=self.theme["secondary"],
                bg=self.theme["bg"]
            )
            or_label.pack(pady=5)
        else:
            goal_var = tk.StringVar()
        
        # Text entry for custom goal
        entry_label = tk.Label(
            goal_window,
            text="Type a new goal:",
            font=("Courier New", 10),
            fg=self.theme["secondary"],
            bg=self.theme["bg"]
        )
        entry_label.pack(pady=5)
        
        goal_entry = tk.Entry(
            goal_window,
            font=("Courier New", 11),
            width=35,
            bg=self.theme["bg"],
            fg=self.theme["primary"]
        )
        goal_entry.pack(pady=5)
        
        def set_goal():
            # Get goal from either dropdown or text entry
            goal = goal_entry.get().strip() or goal_var.get().strip()
            
            if goal:
                self.current_goal = goal
                self.goal_label.config(text=f"📌 {goal}")
                
                # Save to recent goals if new
                if goal not in self.settings["saved_goals"]:
                    self.settings["saved_goals"].insert(0, goal)
                    # Keep only last 10 goals
                    self.settings["saved_goals"] = self.settings["saved_goals"][:10]
                    self.save_settings()
                
                goal_window.destroy()
                # Actually start the timer now
                self.is_running = True
                self.update_timer()
            else:
                self.current_goal = ""
                self.goal_label.config(text="")
                goal_window.destroy()
                # Start anyway without a goal
                self.is_running = True
                self.update_timer()
        
        # Buttons
        button_frame = tk.Frame(goal_window, bg=self.theme["bg"])
        button_frame.pack(pady=20)
        
        start_btn = tk.Button(
            button_frame,
            text="Start ✨",
            command=set_goal,
            bg=self.theme["accent1"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=12
        )
        start_btn.pack(side="left", padx=10)
        
        skip_btn = tk.Button(
            button_frame,
            text="Skip",
            command=lambda: (goal_window.destroy(), setattr(self, 'is_running', True), self.update_timer()),
            bg=self.theme["accent2"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=12
        )
        skip_btn.pack(side="left", padx=10)
        
        # Bind Enter key to set goal
        goal_entry.bind('<Return>', lambda e: set_goal())
        
        # Focus on text entry
        goal_entry.focus()
    
    def start_timer(self):
        if not self.is_running:
            # Show goal popup first
            self.ask_for_goal()
    
    def pause_timer(self):
        self.is_running = False
    
    def reset_timer(self):
        self.is_running = False
        if self.is_work_session:
            self.time_left = self.work_time
        else:
            self.time_left = self.break_time
        self.current_goal = ""
        self.goal_label.config(text="")
        self.update_display()
    
    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self.root.after(1000, self.update_timer)
        elif self.is_running and self.time_left == 0:
            self.timer_finished()
    
    def timer_finished(self):
        """Called when timer reaches 0"""
        self.is_running = False
        
        # Play custom notification sound if enabled
        if self.settings.get("sound_enabled", True):
            self.play_notification_sound()
        
        # Show end message
        self.show_message(random.choice(self.end_messages))
        
        # Increment session counter if work session completed
        if self.is_work_session:
            self.settings["total_sessions_today"] = self.settings.get("total_sessions_today", 0) + 1
            self.settings["last_session_date"] = datetime.now().strftime("%Y-%m-%d")
            self.save_settings()
            self.session_counter_label.config(text=f"Sessions today: {self.settings['total_sessions_today']}")
        
        # Show popup
        self.show_popup()
        
        # Switch session
        self.root.after(2000, self.switch_session)
    
    def play_notification_sound(self):
        """Play the custom notification sound"""
        import os
        
        # Check if custom sound exists
        if os.path.exists(self.sound_path):
            try:
                # Try using pygame for mp3 support
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(self.sound_path)
                pygame.mixer.music.play()
            except:
                try:
                    # Fallback to playsound library
                    from playsound import playsound
                    playsound(self.sound_path, False)
                except:
                    # Final fallback to system beep
                    try:
                        winsound.MessageBeep(winsound.MB_ICONASTERISK)
                    except:
                        print('\a')
        else:
            # No custom sound, use system beep
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                print('\a')
    
    def show_popup(self):
        """Show a gentle popup reminder"""
        popup = tk.Toplevel(self.root)
        popup.title("✨ Timer Complete ✨")
        popup.geometry("300x150")
        popup.configure(bg=self.theme["bg"])
        
        # Center popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 150
        y = (popup.winfo_screenheight() // 2) - 75
        popup.geometry(f'300x150+{x}+{y}')
        
        if self.is_work_session:
            message = "Work session complete!\nTime for a break ☕"
        else:
            message = "Break complete!\nReady when you are 💜"
        
        label = tk.Label(
            popup,
            text=message,
            font=("Courier New", 12),
            fg=self.theme["primary"],
            bg=self.theme["bg"]
        )
        label.pack(pady=30)
        
        button = tk.Button(
            popup,
            text="Okay ✨",
            command=popup.destroy,
            bg=self.theme["accent1"],
            fg=self.theme["primary"],
            font=("Courier New", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        button.pack()
        
        # Auto close after 5 seconds
        popup.after(5000, popup.destroy)
    
    def switch_session(self):
        """Switch between work and break"""
        if self.is_work_session:
            # Switch to break
            self.is_work_session = False
            self.time_left = self.break_time
            self.title_label.config(text="✨ Break Time ✨")
            self.current_goal = ""
            self.goal_label.config(text="")
            self.show_message(random.choice(self.break_messages))
        else:
            # Switch to work
            self.is_work_session = True
            self.time_left = self.work_time
            self.title_label.config(text="✨ Work Time ✨")
            self.current_goal = ""
            self.goal_label.config(text="")
            self.show_message(random.choice(self.start_messages))
        
        self.update_display()
    
    def update_display(self):
        """Update the timer display"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_string)
        
        # Update mini window if it exists
        if self.mini_window and self.mini_window.winfo_exists():
            self.mini_window.update_mini_display(time_string, self.current_goal)
    
    def create_mini_window(self):
        """Create or show the mini always-on-top window"""
        if self.mini_window and self.mini_window.winfo_exists():
            self.mini_window.deiconify()
        else:
            self.mini_window = MiniWindow(self, self.theme)
        
        # Minimize main window
        self.root.iconify()


class MiniWindow(tk.Toplevel):
    def __init__(self, parent_timer, theme):
        super().__init__()
        
        self.parent_timer = parent_timer
        self.theme = theme
        
        # Window setup
        self.title("⏳")
        self.geometry("180x160")  # Increased from 140 to 160 to fit button
        self.configure(bg=theme["bg"])
        self.attributes('-topmost', True)
        self.resizable(False, False)
        
        # Position in top right corner (or saved position)
        saved_pos = parent_timer.settings.get("mini_window_position")
        if saved_pos:
            self.geometry(f'180x160+{saved_pos[0]}+{saved_pos[1]}')
        else:
            self.update_idletasks()
            x = self.winfo_screenwidth() - 200
            y = 20
            self.geometry(f'180x160+{x}+{y}')
        
        # Save position when moved
        self.bind('<Configure>', self.save_position)
        
        # Goal label
        self.goal_label = tk.Label(
            self,
            text="",
            font=("Courier New", 8),
            fg=theme["primary"],
            bg=theme["bg"],
            wraplength=160,
            height=2
        )
        self.goal_label.pack(pady=3)
        
        # Tiny hourglass
        self.canvas = tk.Canvas(
            self,
            width=40,
            height=50,
            bg=theme["bg"],
            highlightthickness=0
        )
        self.canvas.pack(pady=3)
        self.draw_tiny_hourglass()
        
        # Timer text
        self.time_label = tk.Label(
            self,
            text="25:00",
            font=("Courier New", 16, "bold"),
            fg=theme["primary"],
            bg=theme["bg"]
        )
        self.time_label.pack()
        
        # Restore button
        restore_btn = tk.Button(
            self,
            text="Restore",
            command=self.restore_main,
            bg=theme["accent1"],
            fg=theme["primary"],
            font=("Courier New", 8),
            relief="flat",
            cursor="hand2"
        )
        restore_btn.pack(pady=3)
        
    def save_position(self, event):
        """Save mini window position"""
        if event.widget == self:
            self.parent_timer.settings["mini_window_position"] = [self.winfo_x(), self.winfo_y()]
            self.parent_timer.save_settings()
        
    def draw_tiny_hourglass(self):
        """Draw a tiny version of the hourglass"""
        c = self.canvas
        scale = 3
        base_x = 8
        base_y = 5
        
        rim_color = self.theme["accent3"]
        sand_color = self.theme["accent1"]
        
        # Simplified tiny hourglass
        coords_rim_top = [(2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
        coords_glass_top = [(3,2), (4,2), (5,2), (6,2), (4,3), (5,3)]
        coords_middle = [(4,4), (5,4)]
        coords_glass_bottom = [(4,5), (5,5), (3,6), (4,6), (5,6), (6,6)]
        coords_rim_bottom = [(2,7), (3,7), (4,7), (5,7), (6,7), (7,7)]
        
        # Draw all parts
        for x, y in coords_rim_top + coords_rim_bottom:
            c.create_rectangle(
                base_x + x*scale, base_y + y*scale,
                base_x + x*scale + scale, base_y + y*scale + scale,
                fill=rim_color, outline=""
            )
        
        for x, y in coords_glass_top + coords_middle + coords_glass_bottom:
            c.create_rectangle(
                base_x + x*scale, base_y + y*scale,
                base_x + x*scale + scale, base_y + y*scale + scale,
                fill=sand_color, outline=""
            )
        
        # Sparkle
        c.create_rectangle(
            base_x + 1*scale, base_y + 2*scale,
            base_x + 1*scale + scale, base_y + 2*scale + scale,
            fill="#ffd700", outline=""
        )
    
    def update_mini_display(self, time_string, goal):
        """Update the mini window's time and goal display"""
        self.time_label.config(text=time_string)
        if goal:
            self.goal_label.config(text=f"📌 {goal}")
        else:
            self.goal_label.config(text="")
    
    def restore_main(self):
        """Restore the main window"""
        self.parent_timer.root.deiconify()
        self.destroy()


# Create and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
