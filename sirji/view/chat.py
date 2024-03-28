import tkinter as tk
from tkinter import ttk  # Import the ttk module
import os
import queue

from .screen import get_screen_resolution

CHAT_LOCK = 'workspace/.chat_lock'


class ChatApp:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls, root=None, message_queue=None):
        if cls._instance is None and root is not None:
            cls(root, message_queue)
        return cls._instance

    def __init__(self, root, message_queue=None):
        if not self._initialized:
            self._initialized = True
            self.root = root
            self.message_queue = message_queue
            self.root.title("Sirji Chat")

            screen_width, screen_height = get_screen_resolution()
            # Calculate window dimensions and position
            # One-third of the screen width (ensure it's an integer)
            window_width = int((screen_width - 15) // 2)
            # Screen height minus top and bottom margins (ensure it's an integer)
            window_height = int(0.61 * (screen_height))
            x_offset = 5                             # Left margin
            y_offset = 5                             # Top margin

            # Set window size and position
            self.root.geometry(
                f"{window_width}x{window_height}+{x_offset}+{y_offset}")

            self.root.configure(bg='lightgray')

            self.chat_feed_frame = tk.Frame(root, bg='white')
            self.chat_feed_frame.pack(pady=(5, 10), fill=tk.BOTH, expand=True)

            self.chat_feed = tk.Text(
                self.chat_feed_frame, height=20, width=50, wrap=tk.WORD)
            self.chat_feed.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(
                self.chat_feed_frame, command=self.chat_feed.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.chat_feed['yscrollcommand'] = self.scrollbar.set
            self.chat_feed.config(font=("Arial", 14),
                                  bg="#f0f0f0", state=tk.DISABLED)

            # Configure tags for bold and larger font
            self.chat_feed.tag_configure("bold", font=("Arial", 14, "bold"))

            self.input_frame = tk.Frame(root, bg='lightgray')
            self.input_frame.pack(fill=tk.X, padx=5)

            self.input_text = tk.Text(self.input_frame, height=3, width=40)
            self.input_text.pack(side=tk.LEFT, fill=tk.BOTH,
                                 expand=True, pady=(5, 10), padx=(0, 5))
            self.input_text.config(font=("Arial", 14))

            # Setup style for the send button using ttk.Style
            self.send_button_style = ttk.Style()
            self.send_button_style.theme_use('default')

            # Configure the style for the enabled and disabled states
            self.send_button_style.configure('Send.TButton',
                                             font=("Arial", 12),
                                             background='#4CAF50',
                                             foreground='white',
                                             relief=tk.RAISED,
                                             borderwidth=2,
                                             padding=(10, 5))
            self.send_button_style.map('Send.TButton',
                                       background=[('disabled', '#D3D3D3')],
                                       foreground=[('disabled', '#A9A9A9')])

            self.send_button = ttk.Button(
                self.input_frame, text="Send", style='Send.TButton', command=self.send_message)
            self.send_button.pack(side=tk.RIGHT, pady=(5, 10), padx=(5, 0))

            self.root.protocol("WM_DELETE_WINDOW", self.cleanup_on_exit)

    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            if self.message_queue is not None:
                self.message_queue.put(user_input)
            self.update_chat("You> " + user_input)
            self.input_text.delete("1.0", tk.END)

    def update_chat(self, message):
        self.chat_feed.config(state=tk.NORMAL)

        # Insert the whole message first
        self.chat_feed.insert(tk.END, message + "\n")

        # Calculate the length of the whole text in the widget
        end_index = self.chat_feed.index("end-1c")
        # Beginning of the last inserted line
        start_of_line_index = end_index.split('.')[0] + ".0"

        # Calculate prefix length ("Sirji>" or "You>")
        if message.startswith("Sirji>") or message.startswith("You>"):
            prefix_length = message.find('>') + 1

        # Apply the 'bold' tag to the prefix
        self.chat_feed.tag_add("bold", start_of_line_index,
                               f"{start_of_line_index}+{prefix_length}c")

        self.chat_feed.see(tk.END)
        self.chat_feed.config(state=tk.DISABLED)

    def send_system_message(self, message):
        self.update_chat("Sirji> " + message)

    def send_system_message_from_external(self, message):
        if self.root:
            self.root.after(0, lambda: self.send_system_message(message))

    def cleanup_on_exit(self):
        try:
            os.remove(CHAT_LOCK)
        except FileNotFoundError:
            pass
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def set_send_button_state(self, state="normal"):
        # Set button state directly without modifying other styles
        self.send_button.state(['!disabled'] if state ==
                               "normal" else ['disabled'])


def disable_chat_send_button():
    if ChatApp._instance:
        ChatApp._instance.set_send_button_state("disabled")


def enable_chat_send_button():
    if ChatApp._instance:
        ChatApp._instance.set_send_button_state("normal")


def run_chat_app(messages_queue=None):
    if os.path.exists(CHAT_LOCK):
        print("Chat app is already running.")
        return
    else:
        with open(CHAT_LOCK, "w") as f:
            f.write("lock")

    root = tk.Tk()
    ChatApp.get_instance(root, messages_queue).start()


def send_external_system_message(message):
    if ChatApp._instance:
        ChatApp._instance.send_system_message_from_external(message)
