import tkinter as tk
import psutil
import platform
import subprocess
import socket
import csv
import re
import datetime
import sys
import shutil
import os

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("系统硬件信息")
        self.root.geometry("1800x900")  
        self.root.resizable(True, True)
        self.root.configure(bg="#252525")  

        self.title_font = ("微软雅黑", 12, "bold")
        self.content_font = ("微软雅黑", 10)

        main_frame = tk.Frame(root, bg="#252525")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        first_frame = tk.Frame(main_frame, bg="#252525")
        first_frame.grid(row=0, column=0, sticky="nw", padx=(0, 10))

        second_frame = tk.Frame(main_frame, bg="#252525")
        second_frame.grid(row=0, column=1, sticky="nw", padx=(0, 10))

        third_frame = tk.Frame(main_frame, bg="#252525")
        third_frame.grid(row=0, column=2, sticky="nw", padx=(0, 10))

        fourth_frame = tk.Frame(main_frame, bg="#252525")
        fourth_frame.grid(row=0, column=3, sticky="nw", padx=(0, 10))

        fifth_frame = tk.Frame(main_frame, bg="#252525")
        fifth_frame.grid(row=0, column=4, sticky="nw")

        # 第一列
        self.add_info(first_frame, "系统信息")
        self.add_info(first_frame, "CPU详细信息")
        self.add_info(first_frame, "BIOS信息")
        self.add_info(first_frame, "主板信息")
        self.add_info(first_frame, "电池信息")

        # 第二列
        self.add_info(second_frame, "内存信息")
        self.add_info(second_frame, "网卡信息")
        self.add_info(second_frame, "显卡信息")  

        # 第三列
        self.add_info(third_frame, "硬盘信息")
        self.add_info(third_frame, "声卡信息")  

        # 第四列
        self.add_info(fourth_frame, "蓝牙设备信息") 

        # 第五列
        self.add_info(fifth_frame, "Python版本")
        self.add_info(fifth_frame, "PIP版本")
        self.add_info(fifth_frame, "CUDA版本")
        self.add_info(fifth_frame, "PyTorch版本")
        self.add_info(fifth_frame, "TensorFlow版本")
        self.add_info(fifth_frame, "Node.js版本")  
        self.add_info(fifth_frame, "WSL版本")
        self.add_info(fifth_frame, "C++版本")  
        self.add_info(fifth_frame, "Rust版本")

        self.set_static_info()

        # 每10秒更新一次 CPU 和内存使用率
        self.update_dynamic_info()

    def add_info(self, parent, title):
        """在指定父框架中添加信息"""
        # 标题标签
        title_label = tk.Label(
            parent,
            text=f"{title}:",
            font=self.title_font,
            anchor="w",
            bg="#252525",
            fg="#7b6cfc"  # 蓝紫色
        )
        title_label.pack(anchor="w", pady=(10, 0))

        # 内容标签
        content_label = tk.Label(
            parent,
            text="",  
            font=self.content_font,
            anchor="w",
            justify="left",
            bg="#252525",
            fg="#64ff65",  # 绿色
            wraplength=300  
        )
        content_label.pack(anchor="w", pady=(0, 10))

        # 特别处理 "C++版本"
        if title == "C++版本":
            safe_title = "C_plus_plus版本"
        else:
            safe_title = re.sub(r'[^\w]', '_', title)
        setattr(self, f"{safe_title}_label", content_label)

    def set_static_info(self):
        self.系统信息_label.config(text=self.get_system_info())
        self.CPU详细信息_label.config(text=self.get_cpu_details())
        self.BIOS信息_label.config(text=self.get_bios_info())
        self.主板信息_label.config(text=self.get_motherboard_info())
        self.电池信息_label.config(text=self.get_battery_info())
        self.内存信息_label.config(text=self.get_memory_info())
        self.网卡信息_label.config(text=self.get_network_info())
        self.显卡信息_label.config(text=self.get_gpu_info())  
        self.硬盘信息_label.config(text=self.get_disk_info())
        self.声卡信息_label.config(text=self.get_sound_info())  
        self.蓝牙设备信息_label.config(text=self.get_bluetooth_info())  

        self.Python版本_label.config(text=self.get_python_version())
        self.PIP版本_label.config(text=self.get_pip_version())
        self.CUDA版本_label.config(text=self.get_cuda_version())
        self.PyTorch版本_label.config(text=self.get_pytorch_version())
        self.TensorFlow版本_label.config(text=self.get_tensorflow_version())
        self.Node_js版本_label.config(text=self.get_nodejs_version()) 
        self.WSL版本_label.config(text=self.get_wsl_version())
        self.C_plus_plus版本_label.config(text=self.get_cpp_version()) 
        self.Rust版本_label.config(text=self.get_rust_version())

    def update_dynamic_info(self):
        """定期更新 CPU 和内存使用率"""
        new_cpu_usage = self.get_cpu_usage()
        cpu_details = (
            f"序列号: {self.get_cpu_serial_number()}\n"
            f"名称: {self.get_cpu_name()}\n"
            f"核心数: {self.get_cpu_core_count()}\n"
            f"时钟频率: {self.get_cpu_clock_speed()} MHz\n"
            f"已使用: {new_cpu_usage}%\n"
        )
        self.CPU详细信息_label.config(text=cpu_details)

        new_memory_info = self.get_memory_usage()
        memory_details = (
            f"已用内存: {new_memory_info['used']} GB\n"
            f"可用内存: {new_memory_info['available']} GB\n"
            f"内存使用率: {new_memory_info['percent']}%\n"
        )
        self.内存信息_label.config(text=memory_details)

        # 每10秒更新一次
        self.root.after(10000, self.update_dynamic_info)

    def get_system_info(self):
        """获取系统硬件信息，添加系统启动时间"""
        try:
            boot_time_timestamp = psutil.boot_time()
            boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            return (
                f"操作系统名称及版本号: {platform.platform()}\n"
                f"操作系统版本号: {platform.version()}\n"
                f"操作系统位数: {platform.architecture()[0]}\n"
                f"计算机类型: {platform.machine()}\n"
                f"计算机网络名称: {platform.node()}\n"
                f"处理器信息: {platform.processor()}\n"
                f"系统启动时间: {boot_time}\n"
            )
        except Exception as e:
            return f"无法获取系统信息: {e}"

    def get_cpu_details(self):
        """获取 CPU 详细信息，删除温度"""
        try:
            serial_number = self.get_cpu_serial_number()
            name = self.get_cpu_name()
            core_count = self.get_cpu_core_count()
            max_clock_speed = self.get_cpu_clock_speed()
            load_percentage = self.get_cpu_usage()

            return (
                f"序列号: {serial_number}\n"
                f"名称: {name}\n"
                f"核心数: {core_count}\n"
                f"时钟频率: {max_clock_speed} MHz\n"
                f"已使用: {load_percentage}%\n"
            )
        except Exception as e:
            return f"无法获取 CPU 详细信息: {e}"

    def get_cpu_serial_number(self):
        """获取 CPU 序列号"""
        try:
            serial_number = subprocess.check_output(
                "wmic cpu get ProcessorId", shell=True
            ).decode('gbk', 'ignore').split("\n")[1].strip()
            return serial_number if serial_number else "未知"
        except Exception:
            return "未知"

    def get_cpu_name(self):
        """获取 CPU 名称"""
        try:
            name = subprocess.check_output(
                "wmic cpu get Name", shell=True
            ).decode('gbk', 'ignore').split("\n")[1].strip()
            return name if name else "未知"
        except Exception:
            return "未知"

    def get_cpu_core_count(self):
        """获取 CPU 核心数"""
        try:
            core_count = subprocess.check_output(
                "wmic cpu get NumberOfCores", shell=True
            ).decode('gbk', 'ignore').split("\n")[1].strip()
            return core_count if core_count else "未知"
        except Exception:
            return "未知"

    def get_cpu_clock_speed(self):
        """获取 CPU 时钟频率"""
        try:
            max_clock_speed = subprocess.check_output(
                "wmic cpu get MaxClockSpeed", shell=True
            ).decode('gbk', 'ignore').split("\n")[1].strip()
            return max_clock_speed if max_clock_speed else "未知"
        except Exception:
            return "未知"

    def get_cpu_usage(self):
        """获取 CPU 使用率"""
        try:
            return f"{psutil.cpu_percent(interval=1)}"
        except Exception as e:
            return "未知"

    def get_memory_info(self):
        """获取内存详细信息，包括品牌"""
        try:
            memory_output = subprocess.check_output(
                "wmic memorychip get Manufacturer, BankLabel, Capacity, Speed /FORMAT:CSV", shell=True
            ).decode('gbk', 'ignore').strip().split("\n")
            reader = csv.DictReader(memory_output)
            memory_info = ""
            for row in reader:
                manufacturer = row.get("Manufacturer", "未知")
                bank_label = row.get("BankLabel", "未知")
                capacity_bytes = row.get("Capacity", "0")
                speed = row.get("Speed", "未知")

                try:
                    capacity_gb = int(capacity_bytes) / (1024 ** 3)
                except ValueError:
                    capacity_gb = 0

                memory_info += (
                    f"制造商: {manufacturer}\n"
                    f"插槽: {bank_label}\n"
                    f"容量: {capacity_gb:.2f} GB\n"
                    f"速度: {speed} MHz\n\n"
                )

            # 获取系统内存
            mem = psutil.virtual_memory()
            total_memory = mem.total / (1024 ** 3)  # 转为 GB
            used_memory = mem.used / (1024 ** 3)
            available_memory = mem.available / (1024 ** 3)
            percent = mem.percent

            memory_info += (
                f"总内存使用情况:\n"
                f"  已用内存: {used_memory:.2f} GB\n"
                f"  可用内存: {available_memory:.2f} GB\n"
                f"  内存使用率: {percent}%\n"
            )
            return memory_info
        except Exception as e:
            return f"无法获取内存信息: {e}"

    def get_memory_usage(self):
        """获取内存使用率，仅更新使用率相关信息"""
        try:
            mem = psutil.virtual_memory()
            used_memory = mem.used / (1024 ** 3)
            available_memory = mem.available / (1024 ** 3)
            percent = mem.percent

            return {
                'used': f"{used_memory:.2f}",
                'available': f"{available_memory:.2f}",
                'percent': f"{percent}"
            }
        except Exception as e:
            return {'used': "未知", 'available': "未知", 'percent': "未知"}

    def get_disk_info(self):
        """获取硬盘信息，直接显示物理硬盘的信息，不进行分区映射"""
        try:
            disk_output = subprocess.check_output(
                "wmic diskdrive get DeviceID, Manufacturer, Model, Size /FORMAT:CSV", shell=True
            ).decode('gbk', 'ignore').strip().split("\n")
            reader = csv.DictReader(disk_output)
            disk_data = list(reader)

            disk_info = ""
            for disk in disk_data:
                manufacturer = disk.get("Manufacturer", "未知")
                model = disk.get("Model", "未知")
                size_bytes = disk.get("Size", "0")
                device_id = disk.get("DeviceID", "").strip()

                try:
                    size_gb = int(size_bytes) / (1024 ** 3)
                except ValueError:
                    size_gb = 0

                disk_info += (
                    f"设备ID: {device_id}\n"
                    f"制造商: {manufacturer}\n"
                    f"型号: {model}\n"
                    f"容量: {size_gb:.2f} GB\n\n"
                )
            if not disk_info.strip():
                disk_info = "没有检测到硬盘信息"
            return disk_info
        except Exception as e:
            return f"无法获取硬盘信息: {e}"

    def get_gpu_info(self):
        """获取显卡信息，仅显示显卡名称"""
        try:
            result = subprocess.check_output(
                "wmic path win32_videocontroller get Caption /FORMAT:CSV", shell=True
            ).decode("gbk", "ignore").strip().split("\n")[1:]
            gpus = [gpu.split(',')[-1].strip() for gpu in result if gpu.strip()]
            gpu_info = ""
            if gpus:
                gpu_info += f"检测到 {len(gpus)} 个显卡:\n"
                for idx, gpu in enumerate(gpus, 1):
                    gpu_info += f"  {idx}. {gpu}\n"
            else:
                gpu_info = "没有检测到显卡设备"
            return gpu_info
        except Exception as e:
            return f"无法获取显卡信息: {e}"

    def get_sound_info(self):
        """获取声卡信息，分类显示播放设备、录音设备、虚拟设备"""
        try:
            sound_output = subprocess.check_output(
                "wmic sounddev get Caption, ProductName, Status /FORMAT:CSV", shell=True
            ).decode('gbk', 'ignore').strip().split("\n")
            reader = csv.DictReader(sound_output)
            playback = []
            recording = []
            virtual = []
            others = []

            for row in reader:
                caption = row.get("Caption", "").lower()
                product_name = row.get("ProductName", "").lower()
                status = row.get("Status", "未知")

                device_info = f"{row.get('Caption', '未知')} (状态: {status})"

                if any(keyword in caption or keyword in product_name for keyword in ["speaker", "headphones", "playback"]):
                    playback.append(device_info)
                elif any(keyword in caption or keyword in product_name for keyword in ["microphone", "record", "input"]):
                    recording.append(device_info)
                elif any(keyword in caption or keyword in product_name for keyword in ["virtual", "stereo mix", "voice changer"]):
                    virtual.append(device_info)
                else:
                    others.append(device_info)

            sound_info = ""

            if playback:
                sound_info += "播放设备:\n"
                for idx, device in enumerate(playback, 1):
                    sound_info += f"  {idx}. {device}\n"
                sound_info += "\n"

            if recording:
                sound_info += "录音设备:\n"
                for idx, device in enumerate(recording, 1):
                    sound_info += f"  {idx}. {device}\n"
                sound_info += "\n"

            if virtual:
                sound_info += "虚拟设备:\n"
                for idx, device in enumerate(virtual, 1):
                    sound_info += f"  {idx}. {device}\n"
                sound_info += "\n"

            if others:
                sound_info += "其他设备:\n"
                for idx, device in enumerate(others, 1):
                    sound_info += f"  {idx}. {device}\n"
                sound_info += "\n"

            if not sound_info.strip():
                sound_info = "没有检测到声卡设备"

            return sound_info
        except Exception as e:
            return f"无法获取声卡信息: {e}"

    def get_bluetooth_info(self):
        """获取蓝牙设备信息，过滤无关条目"""
        try:
            command = 'Get-PnpDevice -Class Bluetooth | Select-Object -Property Name, Status'
            output = subprocess.check_output(['powershell', '-NoProfile', '-Command', command], stderr=subprocess.STDOUT).decode('gbk', 'ignore').strip().split('\n')

            exclude_keywords = ['---', '通用属性配置文件', '设备信息服务', '通用访问配置文件']

            devices = [
                line.strip() for line in output 
                if line.strip() and not line.startswith('Name') and not any(keyword in line for keyword in exclude_keywords)
            ]

            bluetooth_info = ""

            if devices:
                bluetooth_info += f"检测到 {len(devices)} 个蓝牙设备:\n"
                for idx, device in enumerate(devices, 1):
                    parts = re.split(r'\s{2,}', device)
                    if len(parts) >= 2:
                        name, status = parts[0], parts[1]
                        bluetooth_info += f"  {idx}. {name} (状态: {status})\n"
                    else:
                        bluetooth_info += f"  {idx}. {device} (状态: 未知)\n"
            else:
                bluetooth_info = "没有检测到蓝牙设备"

            return bluetooth_info
        except Exception as e:
            return f"无法获取蓝牙设备信息: {e}"

    def get_python_version(self):
        """获取Python版本"""
        try:
            python_version = platform.python_version()
            return python_version
        except Exception:
            return "未查询到"

    def get_pip_version(self):
        """获取PIP版本"""
        try:
            pip_version = subprocess.check_output(
                [sys.executable, "-m", "pip", "--version"], stderr=subprocess.STDOUT
            ).decode('gbk', 'ignore').strip()
            return pip_version
        except Exception:
            return "未安装"

    def get_cuda_version(self):
        """获取CUDA版本"""
        try:
            nvcc_path = shutil.which("nvcc")
            if nvcc_path:
                output = subprocess.check_output(["nvcc", "--version"], stderr=subprocess.STDOUT).decode('gbk', 'ignore')
                match = re.search(r"release\s+(\d+\.\d+)", output)
                if match:
                    return f"CUDA {match.group(1)}"
                else:
                    return "未查询到"
            else:
                return "未安装"
        except Exception:
            return "未查询到"

    def get_pytorch_version(self):
        """获取PyTorch版本"""
        try:
            import torch
            return torch.__version__
        except ImportError:
            return "未安装"

    def get_tensorflow_version(self):
        """获取TensorFlow版本"""
        try:
            import tensorflow as tf
            return tf.__version__
        except ImportError:
            return "未安装"

    def get_nodejs_version(self):
        """获取Node.js版本"""
        try:
            node_version = subprocess.check_output(
                ["node", "--version"], stderr=subprocess.STDOUT
            ).decode('gbk', 'ignore').strip()
            return node_version
        except Exception:
            return "未安装"

    def get_wsl_version(self):
        """获取WSL版本"""
        try:
            wsl_version = subprocess.check_output(
                ["wsl.exe", "--version"], stderr=subprocess.STDOUT
            ).decode('gbk', 'ignore').strip()
            if not wsl_version:
                return "未查询到"
            return wsl_version
        except Exception:
            return "未安装"

    def get_cpp_version(self):
        """获取C++版本"""
        try:
            gpp_path = shutil.which("g++")
            if gpp_path:
                output = subprocess.check_output(["g++", "--version"], stderr=subprocess.STDOUT).decode('gbk', 'ignore')
                first_line = output.split("\n")[0]
                return first_line
            cl_path = shutil.which("cl.exe")
            if cl_path:
                output = subprocess.check_output([cl_path], stderr=subprocess.STDOUT, shell=True).decode('gbk', 'ignore')
                match = re.search(r"Compiler Version (\d+\.\d+)", output)
                if match:
                    return f"MSVC {match.group(1)}"
                else:
                    return "未查询到"
            return "未安装"
        except Exception:
            return "未查询到"

    def get_rust_version(self):
        """获取Rust版本"""
        try:
            rustc_path = shutil.which("rustc")
            if rustc_path:
                output = subprocess.check_output(["rustc", "--version"], stderr=subprocess.STDOUT).decode('gbk', 'ignore').strip()
                return output
            else:
                return "未安装"
        except Exception:
            return "未查询到"

    def get_bios_info(self):
        """获取 BIOS 信息"""
        try:
            bios_output = subprocess.check_output(
                "wmic bios get Manufacturer, Name, Version, ReleaseDate /FORMAT:CSV", shell=True
            ).decode('gbk', 'ignore').strip().split("\n")
            reader = csv.DictReader(bios_output)
            bios_data = ""
            for row in reader:
                manufacturer = row.get("Manufacturer", "未知")
                name = row.get("Name", "未知")
                version = row.get("Version", "未知")
                release_date = row.get("ReleaseDate", "未知")
                bios_data += (
                    f"制造商: {manufacturer}\n"
                    f"名称: {name}\n"
                    f"版本: {version}\n"
                    f"发布日期: {self.format_wmi_date(release_date)}\n\n"
                )
            if not bios_data.strip():
                bios_data = "没有检测到 BIOS 信息"
            return bios_data
        except Exception as e:
            return f"无法获取 BIOS 信息: {e}"

    def get_motherboard_info(self):
        """获取主板信息"""
        try:
            motherboard_output = subprocess.check_output(
                "wmic baseboard get Manufacturer, Product, Version /FORMAT:CSV", shell=True
            ).decode('gbk', 'ignore').strip().split("\n")
            reader = csv.DictReader(motherboard_output)
            motherboard_data = ""
            for row in reader:
                manufacturer = row.get("Manufacturer", "未知")
                product = row.get("Product", "未知")
                version = row.get("Version", "未知")
                motherboard_data += (
                    f"制造商: {manufacturer}\n"
                    f"产品: {product}\n"
                    f"版本: {version}\n\n"
                )
            if not motherboard_data.strip():
                motherboard_data = "没有检测到主板信息"
            return motherboard_data
        except Exception as e:
            return f"无法获取主板信息: {e}"

    def get_battery_info(self):
        """获取电池信息"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                secsleft = battery.secsleft
                power_plugged = battery.power_plugged
                if secsleft == psutil.POWER_TIME_UNLIMITED:
                    timeleft = "无限"
                elif secsleft == psutil.POWER_TIME_UNKNOWN:
                    timeleft = "未知"
                else:
                    hours = secsleft // 3600
                    minutes = (secsleft % 3600) // 60
                    timeleft = f"{hours}小时 {minutes}分钟"
                status = "已连接电源" if power_plugged else "未连接电源"
                battery_info = (
                    f"电池电量: {percent}%\n"
                    f"剩余时间: {timeleft}\n"
                    f"电源状态: {status}\n"
                )
            else:
                battery_info = "没有检测到电池信息"
            return battery_info
        except Exception as e:
            return f"无法获取电池信息: {e}"

    def get_network_info(self):
        """获取网卡信息"""
        try:
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            network_info = ""
            for iface, addrs in net_if_addrs.items():
                status = "已启用" if net_if_stats[iface].isup else "已禁用"
                network_info += f"{iface} ({status}):\n"
                for addr in addrs:
                    if addr.family == socket.AF_LINK:
                        network_info += f"  MAC地址: {addr.address}\n"
                    elif addr.family == socket.AF_INET:
                        network_info += f"  IP地址: {addr.address} 子网掩码: {addr.netmask}\n"
            return network_info
        except Exception as e:
            return f"无法获取网卡信息: {e}"

    def format_wmi_date(self, wmi_date):
        try:
            if not wmi_date or wmi_date == "NULL":
                return "未知"
            date_str = wmi_date.split('.')[0]  # 去除毫秒和时区
            dt = datetime.datetime.strptime(date_str, "%Y%m%d%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return "未知"

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemInfoApp(root)
    root.mainloop()
