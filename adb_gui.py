import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog

class ADBGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB 图形界面")

        self.label = tk.Label(root, text="安装 APK")
        self.label.pack()

        self.install_button = tk.Button(root, text="安装", command=self.install_apk, state=tk.DISABLED)
        self.install_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.check_device_button = tk.Button(root, text="检查设备", command=self.check_device)
        self.check_device_button.pack()

        self.root.after(1000, self.check_device_periodically)

    def get_adb_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, 'adb')

    def check_device(self):
        adb_path = self.get_adb_path()
        try:
            result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
            devices_output = result.stdout
            if "List of devices attached" in devices_output:
                devices_output = devices_output.replace("List of devices attached", "已连接的设备列表")
                if "\tdevice" in devices_output:
                    devices_output = devices_output.replace("\tdevice", "\t设备已连接")
                    self.install_button.config(state=tk.NORMAL)
                else:
                    devices_output += "\n未检测到任何设备"
                    self.install_button.config(state=tk.DISABLED)
            self.status_label.config(text=devices_output)
        except Exception as e:
            self.status_label.config(text=f"检测设备时出错: {e}")
            self.install_button.config(state=tk.DISABLED)

    def check_device_periodically(self):
        self.check_device()
        self.root.after(1000, self.check_device_periodically)

    def install_apk(self):
        adb_path = self.get_adb_path()
        apk_path = filedialog.askopenfilename(title="选择APK文件", filetypes=[("APK文件", "*.apk")])
        if apk_path:
            try:
                result = subprocess.run([adb_path, 'install', apk_path], capture_output=True, text=True)
                install_output = result.stdout
                if "Performing Streamed Install" in install_output:
                    install_output = install_output.replace("Performing Streamed Install", "正在执行流式安装")
                if "Success" in install_output:
                    install_output = install_output.replace("Success", "安装成功")
                self.status_label.config(text=install_output)
            except Exception as e:
                self.status_label.config(text=f"安装 APK 时出错: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ADBGUI(root)
    root.mainloop()
