import tkinter as tk
from tkinter import scrolledtext
from AudioManager import AudioManager
from ChatManager import ChatManager
from ConfigManager import ConfigManager
import threading


class VoiceChatApp:
    def __init__(self, master):
        self.master = master
        self.config_manager = ConfigManager()
        self.audio_manager = AudioManager()
        self.chat_manager = ChatManager(self.config_manager.get_api_key())

        self.master.title("Voice Chat with ChatGPT")
        self.master.geometry('800x500')  # Adjust window size
        self.master.configure(bg='#36393F')  # Discord's dark background color

        self.setup_ui()

    def setup_ui(self):
        # Frame for buttons and status
        top_frame = tk.Frame(self.master, bg='#2F3136', pady=10, padx=10)
        top_frame.grid(row=0, sticky='ew', padx=10)
        top_frame.grid_columnconfigure([0, 1], weight=1)

        # Start/Stop Recording Button
        self.record_button = tk.Button(top_frame, text="Start Recording", command=self.toggle_recording,
                                       font=('Calibri', 14, 'bold'), bg='#5865F2', fg='white', relief='ridge')
        self.record_button.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

        # Clear Chat Button
        self.clear_button = tk.Button(top_frame, text="Clear Chat", command=self.clear_chat,
                                      font=('Calibri', 14, 'bold'), bg='#5865F2', fg='white', relief='ridge')
        self.clear_button.grid(row=0, column=1, sticky='ew', padx=10, pady=5)

        # Text display for conversation
        self.conversation_text = scrolledtext.ScrolledText(self.master, wrap='word', bg='#40444B', fg='#CCCCCC',
                                                           font=('Consolas', 11), borderwidth=2, relief="sunken")
        self.conversation_text.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.conversation_text.configure(state='disabled')  # Disable editing

        # Status label
        self.status_label = tk.Label(self.master, text="Ready to record", bg='#2F3136', fg='white',
                                     font=('Calibri', 12))
        self.status_label.grid(row=2, column=0, sticky='ew', padx=10, pady=5)

        # Configure resizing behavior
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def toggle_recording(self):
        if self.record_button.cget('text') == "Start Recording":
            self.record_button.config(text="Stop Recording", bg='#E06C75')
            self.start_recording()
        else:
            self.record_button.config(text="Start Recording", bg='#5865F2')
            self.stop_recording()

    def start_recording(self):
        self.status_label.config(text="Recording...")
        threading.Thread(target=self.process_audio).start()

    def stop_recording(self):
        self.status_label.config(text="Recording stopped. Processing...")

    def clear_chat(self):
        self.conversation_text.configure(state='normal')
        self.conversation_text.delete('1.0', tk.END)
        self.conversation_text.configure(state='disabled')
        self.status_label.config(text="Chat cleared")

    def process_audio(self):
        filename = "input.wav"
        self.audio_manager.record_audio(filename)
        text = self.audio_manager.recognize_speech(filename)
        if text:
            response = self.chat_manager.get_response(text)
            self.display_conversation("You: " + text)
            self.display_conversation("ChatGPT: " + response)
            self.chat_manager.text_to_speech(response)
        self.stop_recording()

    def display_conversation(self, message):
        self.conversation_text.configure(state='normal')
        self.conversation_text.insert(tk.END, message + "\n")
        self.conversation_text.configure(state='disabled')
        self.conversation_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceChatApp(root)
    root.mainloop()
