import tkinter as tk
from pythonping import ping
import psutil

# Variables globales pour le déplacement
drag_data = {"x": 0, "y": 0, "widget": None}
root = None  # Déclaration de root comme variable globale


def get_network_usage():
    # Obtenir les statistiques d'utilisation du réseau
    network_stats = psutil.net_io_counters()

    # Obtenir les octets téléchargés et téléversés
    bytes_sent = network_stats.bytes_sent
    bytes_received = network_stats.bytes_recv

    # Convertir les octets en mégaoctets (Mo)
    megabytes_sent = bytes_sent / (1024 * 1024)
    megabytes_received = bytes_received / (1024 * 1024)

    # Retourner les statistiques d'utilisation du réseau
    return megabytes_sent, megabytes_received


# Fonction pour commencer le déplacement
def start_drag(event):
    drag_data["x"] = event.x
    drag_data["y"] = event.y
    drag_data["widget"] = event.widget


# Fonction pour effectuer le déplacement
def drag(event):
    widget = drag_data["widget"]
    x = widget.winfo_rootx() - drag_data["x"] + event.x
    y = widget.winfo_rooty() - drag_data["y"] + event.y
    root.geometry(f"+{x}+{y}")


# Fonction pour arrêter le déplacement
def stop_drag(event):
    drag_data["widget"] = None


def create_widget():
    global root

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")
    root.overrideredirect(True)
    root.configure(bg="black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    widget_width = 250
    widget_height = 60
    x_position = (screen_width - widget_width) // 2 + 400
    y_position = screen_height - widget_height + 15
    root.geometry(f"{widget_width}x{widget_height}+{int(x_position)}+{int(y_position)}")

    stats_text = tk.Text(root, font=("Segoe UI", 10), fg="white", bg="black", height=1, borderwidth=0)
    stats_text.pack(pady=10, padx=10)

    # Ajout des événements de déplacement au widget
    stats_text.bind("<ButtonPress-1>", start_drag)
    stats_text.bind("<B1-Motion>", drag)
    stats_text.bind("<ButtonRelease-1>", stop_drag)

    def update_stats():
        response_list = ping('google.com', count=1)

        if response_list.rtt_avg_ms is not None:
            ping_value = response_list.rtt_avg_ms

            if ping_value < 30:
                ping_color = "lime"
            elif ping_value > 100:
                ping_color = "red"
            else:
                ping_color = "white"

            memory_percent = psutil.virtual_memory().percent

            stats_text.delete("1.0", tk.END)

            stats_text.insert(tk.END, f"Ping: ")
            stats_text.insert(tk.END, f"{ping_value} ms", "ping_color")

            stats_text.insert(tk.END, f"  |  Memory: ")
            if memory_percent >= 90:
                stats_text.insert(tk.END, f"{memory_percent:.1f}%", "red_color")
            else:
                stats_text.insert(tk.END, f"{memory_percent:.1f}%", "white_color")

            stats_text.tag_configure("ping_color", foreground=ping_color)
            stats_text.tag_configure("red_color", foreground="red")
            stats_text.tag_configure("white_color", foreground="white")

        else:
            stats_text.delete("1.0", tk.END)
            stats_text.insert(tk.END, "Ping: N/A  |  Memory: N/A", "default")

        root.after(1000, update_stats)

    update_stats()

    def keep_on_top():
        root.attributes("-topmost", True)
        root.after(100, keep_on_top)

    keep_on_top()

    root.mainloop()


create_widget()
