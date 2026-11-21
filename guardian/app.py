

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from guardian.scanner import scan_environment
from guardian.dependency_engine import analyze_dependencies
from guardian.compatibility import analyze_compatibility
from guardian.installer import install_tool
from guardian.database import get_installation_history


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

class GuardianApp:

    def __init__(self, root):

        self.root = root
        self.root.title("eSim Toolchain Guardian")
        self.root.geometry("1200x750")
        self.root.minsize(950, 600)
        self.root.configure(bg="#101827")

        self.scan_result = None
        self.dependency_result = None
        self.compatibility_result = None

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()

        self.scan_environment_async()

    # --------------------------------------------------
    # STYLES
    # --------------------------------------------------

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1c293b",
            foreground="white",
            fieldbackground="#1c293b",
            rowheight=32,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#26364d",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#2563eb")]
        )

    # --------------------------------------------------
    # MAIN LAYOUT
    # --------------------------------------------------

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#172235",
            width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="eSim Guardian",
            bg="#172235",
            fg="white",
            font=("Arial", 19, "bold")
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="Automated Tool Manager",
            bg="#172235",
            fg="#94a3b8",
            font=("Arial", 9)
        ).pack(pady=(0, 30))

        self.nav_button(
            "Dashboard",
            self.show_dashboard
        )

        self.nav_button(
            "Environment Scanner",
            self.show_environment_scanner
        )

        self.nav_button(
            "Dependency Analysis",
            self.show_dependency_analysis
        )

        self.nav_button(
            "Compatibility",
            self.show_compatibility
        )

        self.nav_button(
            "Installation Manager",
            self.show_installation_manager
        )

        self.nav_button(
            "Installation History",
            self.show_installation_history
        )

        self.main_area = tk.Frame(
            self.root,
            bg="#101827"
        )
        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

    # --------------------------------------------------
    # NAVIGATION BUTTONS
    # --------------------------------------------------

    def nav_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg="#172235",
            fg="#cbd5e1",
            activebackground="#26364d",
            activeforeground="white",
            font=("Arial", 10),
            anchor="w",
            relief="flat",
            padx=25,
            pady=14,
            cursor="hand2"
        )

        button.pack(fill="x", padx=10, pady=3)

    # --------------------------------------------------
    # PAGE HELPERS
    # --------------------------------------------------

    def clear_page(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_page_title(self, title, description):

        tk.Label(
            self.main_area,
            text=title,
            bg="#101827",
            fg="white",
            font=("Arial", 23, "bold")
        ).pack(anchor="w", padx=30, pady=(30, 5))

        tk.Label(
            self.main_area,
            text=description,
            bg="#101827",
            fg="#94a3b8",
            font=("Arial", 10)
        ).pack(anchor="w", padx=30, pady=(0, 25))

    def create_card(self, parent, title, value, color="#38bdf8"):

        card = tk.Frame(
            parent,
            bg="#1c293b",
            padx=20,
            pady=20
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        tk.Label(
            card,
            text=title,
            bg="#1c293b",
            fg="#94a3b8",
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Label(
            card,
            text=str(value),
            bg="#1c293b",
            fg=color,
            font=("Arial", 25, "bold")
        ).pack(anchor="w", pady=(10, 0))

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    def show_dashboard(self):

        self.clear_page()

        self.create_page_title(
            "Dashboard",
            "Overview of your eSim development environment"
        )

        card_frame = tk.Frame(
            self.main_area,
            bg="#101827"
        )
        card_frame.pack(fill="x", padx=20, pady=10)

        if self.scan_result:

            tools = self.scan_result.get("tools", [])

            installed = sum(
                1 for tool in tools
                if tool.get("status") == "Installed"
            )

            missing = len(tools) - installed

        else:
            installed = 0
            missing = 0

        self.create_card(
            card_frame,
            "INSTALLED TOOLS",
            installed,
            "#22c55e"
        )

        self.create_card(
            card_frame,
            "MISSING TOOLS",
            missing,
            "#f87171"
        )

        health = 0

        if self.dependency_result:
            health = self.dependency_result.get(
                "health_score", 0
            )

        self.create_card(
            card_frame,
            "DEPENDENCY HEALTH",
            f"{health}%",
            "#38bdf8"
        )

        info_frame = tk.Frame(
            self.main_area,
            bg="#1c293b",
            padx=25,
            pady=25
        )
        info_frame.pack(
            fill="x",
            padx=30,
            pady=30
        )

        tk.Label(
            info_frame,
            text="System Information",
            bg="#1c293b",
            fg="white",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 15))

        if self.scan_result:

            system = self.scan_result.get("system", {})

            details = [
                f"Operating System: {system.get('os', 'Unknown')}",
                f"OS Version: {system.get('release', 'Unknown')}",
                f"Architecture: {system.get('architecture', 'Unknown')}",
                f"Python Version: {system.get('python_version', 'Unknown')}"
            ]

        else:
            details = ["System information is not available yet."]

        for detail in details:

            tk.Label(
                info_frame,
                text=detail,
                bg="#1c293b",
                fg="#cbd5e1",
                font=("Arial", 11)
            ).pack(anchor="w", pady=5)

        tk.Button(
            self.main_area,
            text="Scan Environment",
            command=self.scan_environment_async,
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=20,
            pady=12,
            cursor="hand2"
        ).pack(anchor="w", padx=30)

    # --------------------------------------------------
    # ENVIRONMENT SCANNER
    # --------------------------------------------------

    def scan_environment_async(self):

        self.status_message = "Scanning environment..."

        thread = threading.Thread(
            target=self.perform_scan,
            daemon=True
        )
        thread.start()

    def perform_scan(self):

        try:

            result = scan_environment()

            dependency_result = analyze_dependencies(result)
            compatibility_result = analyze_compatibility(result)

            self.root.after(
                0,
                lambda: self.update_scan_results(
                    result,
                    dependency_result,
                    compatibility_result
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.show_error(str(error))
            )

    def update_scan_results(
        self,
        result,
        dependency_result,
        compatibility_result
    ):

        self.scan_result = result
        self.dependency_result = dependency_result
        self.compatibility_result = compatibility_result

        if self.main_area.winfo_children():
            self.show_dashboard()

    def show_environment_scanner(self):

        self.clear_page()

        self.create_page_title(
            "Environment Scanner",
            "Check installed development tools and their versions"
        )

        tk.Button(
            self.main_area,
            text="Refresh Scan",
            command=self.scan_environment_async,
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=18,
            pady=10
        ).pack(anchor="w", padx=30, pady=(0, 20))

        columns = (
            "name",
            "status",
            "version",
            "path"
        )

        table = ttk.Treeview(
            self.main_area,
            columns=columns,
            show="headings"
        )

        headings = {
            "name": "TOOL",
            "status": "STATUS",
            "version": "VERSION",
            "path": "LOCATION"
        }

        for column in columns:
            table.heading(column, text=headings[column])

        table.column("name", width=150)
        table.column("status", width=130)
        table.column("version", width=150)
        table.column("path", width=400)

        table.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        if self.scan_result:

            for tool in self.scan_result.get("tools", []):

                table.insert(
                    "",
                    "end",
                    values=(
                        tool.get("name", ""),
                        tool.get("status", ""),
                        tool.get("version", ""),
                        tool.get("path", "")
                    )
                )

        else:

            tk.Label(
                self.main_area,
                text="Scanning environment. Please wait...",
                bg="#101827",
                fg="#94a3b8"
            ).pack(pady=10)

    # --------------------------------------------------
    # DEPENDENCY ANALYSIS
    # --------------------------------------------------

    def show_dependency_analysis(self):

        self.clear_page()

        self.create_page_title(
            "Dependency Analysis",
            "Check whether your development workflows have all required tools"
        )

        if not self.dependency_result:

            tk.Label(
                self.main_area,
                text="Please scan the environment first.",
                bg="#101827",
                fg="#f87171",
                font=("Arial", 12)
            ).pack(padx=30, pady=20)

            return

        result = self.dependency_result

        self.create_card(
            self.main_area,
            "DEPENDENCY HEALTH",
            f"{result.get('health_score', 0)}%",
            "#38bdf8"
        )

        self.create_card(
            self.main_area,
            "MISSING TOOLS",
            result.get("missing_count", 0),
            "#f87171"
        )

        tk.Label(
            self.main_area,
            text="Workflow Analysis",
            bg="#101827",
            fg="white",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=30, pady=(35, 15))

        for profile in result.get("profiles", []):

            health = profile.get("health", "Unknown")

            color = (
                "#22c55e"
                if health == "Healthy"
                else "#f87171"
            )

            frame = tk.Frame(
                self.main_area,
                bg="#1c293b",
                padx=20,
                pady=15
            )
            frame.pack(fill="x", padx=30, pady=7)

            tk.Label(
                frame,
                text=profile.get("name", ""),
                bg="#1c293b",
                fg="white",
                font=("Arial", 12, "bold")
            ).pack(anchor="w")

            tk.Label(
                frame,
                text=f"Status: {health}",
                bg="#1c293b",
                fg=color,
                font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=5)

            missing = profile.get("missing", [])

            missing_text = (
                ", ".join(missing)
                if missing
                else "None"
            )

            tk.Label(
                frame,
                text=f"Missing dependencies: {missing_text}",
                bg="#1c293b",
                fg="#94a3b8",
                font=("Arial", 10)
            ).pack(anchor="w")

    # --------------------------------------------------
    # COMPATIBILITY CHECKER
    # --------------------------------------------------

    def show_compatibility(self):

        self.clear_page()

        self.create_page_title(
            "Compatibility Checker",
            "Compare installed tool versions with configured minimum versions"
        )

        if not self.compatibility_result:

            tk.Label(
                self.main_area,
                text="Please scan the environment first.",
                bg="#101827",
                fg="#f87171"
            ).pack(padx=30, pady=20)

            return

        result = self.compatibility_result

        summary = tk.Frame(
            self.main_area,
            bg="#101827"
        )
        summary.pack(fill="x", padx=20, pady=10)

        self.create_card(
            summary,
            "TOTAL TOOLS",
            result.get("total", 0)
        )

        self.create_card(
            summary,
            "COMPATIBLE",
            result.get("compatible", 0),
            "#22c55e"
        )

        self.create_card(
            summary,
            "INCOMPATIBLE",
            result.get("incompatible", 0),
            "#f87171"
        )

        columns = (
            "tool",
            "installed",
            "minimum",
            "recommended",
            "status"
        )

        table = ttk.Treeview(
            self.main_area,
            columns=columns,
            show="headings"
        )

        headings = {
            "tool": "TOOL",
            "installed": "INSTALLED VERSION",
            "minimum": "MINIMUM VERSION",
            "recommended": "RECOMMENDED VERSION",
            "status": "STATUS"
        }

        for column in columns:
            table.heading(column, text=headings[column])

        table.column("tool", width=130)
        table.column("installed", width=140)
        table.column("minimum", width=140)
        table.column("recommended", width=160)
        table.column("status", width=130)

        table.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        for item in result.get("results", []):

            table.insert(
                "",
                "end",
                values=(
                    item.get("tool_id", ""),
                    item.get("installed_version", ""),
                    item.get("minimum_version", ""),
                    item.get("recommended_version", ""),
                    item.get("status", "")
                )
            )

    # --------------------------------------------------
    # INSTALLATION MANAGER
    # --------------------------------------------------

    def show_installation_manager(self):

        self.clear_page()

        self.create_page_title(
            "Installation Manager",
            "Install and manage supported eSim development tools"
        )

        tk.Label(
            self.main_area,
            text="Supported tools",
            bg="#101827",
            fg="white",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=30, pady=10)

        self.install_status_labels = {}

        for tool_id, tool_name in [
            ("ngspice", "Ngspice"),
            ("kicad", "KiCad")
        ]:

            frame = tk.Frame(
                self.main_area,
                bg="#1c293b",
                padx=20,
                pady=20
            )

            frame.pack(
                fill="x",
                padx=30,
                pady=10
            )

            tk.Label(
                frame,
                text=tool_name,
                bg="#1c293b",
                fg="white",
                font=("Arial", 14, "bold")
            ).pack(side="left")

            status_label = tk.Label(
                frame,
                text="Checking...",
                bg="#1c293b",
                fg="#94a3b8",
                font=("Arial", 10)
            )

            status_label.pack(side="left", padx=25)

            self.install_status_labels[tool_id] = status_label

            tk.Button(
                frame,
                text=f"Install {tool_name}",
                command=lambda tid=tool_id, name=tool_name:
                    self.start_installation(tid, name),
                bg="#2563eb",
                fg="white",
                relief="flat",
                padx=15,
                pady=9
            ).pack(side="right")

        self.refresh_installation_status()

    def refresh_installation_status(self):

        if not self.scan_result:
            self.scan_environment_async()
            return

        tools = self.scan_result.get("tools", [])

        for tool in tools:

            tool_id = tool.get("id")

            if tool_id in self.install_status_labels:

                status = tool.get("status", "Unknown")

                color = (
                    "#22c55e"
                    if status == "Installed"
                    else "#f87171"
                )

                self.install_status_labels[tool_id].config(
                    text=status,
                    fg=color
                )

    def start_installation(self, tool_id, tool_name):

        confirm = messagebox.askyesno(
            "Confirm Installation",
            f"Do you want to install {tool_name}?\n\n"
            "This requires administrator permission."
        )

        if not confirm:
            return

        if tool_id in self.install_status_labels:
            self.install_status_labels[tool_id].config(
                text="Installing...",
                fg="#38bdf8"
            )

        thread = threading.Thread(
            target=self.perform_installation,
            args=(tool_id, tool_name),
            daemon=True
        )

        thread.start()

    def perform_installation(self, tool_id, tool_name):

        try:

            result = install_tool(tool_id)

            self.root.after(
                0,
                lambda: self.finish_installation(
                    tool_name,
                    result
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.show_error(str(error))
            )

    def finish_installation(self, tool_name, result):

        success = result.get("success", False)
        message = result.get("message", "Unknown result")

        if success:

            messagebox.showinfo(
                "Installation Result",
                f"{tool_name}: {message}"
            )

        else:

            messagebox.showerror(
                "Installation Failed",
                f"{tool_name}: {message}"
            )

        self.scan_environment_async()
        self.show_installation_manager()

    # --------------------------------------------------
    # INSTALLATION HISTORY
    # --------------------------------------------------

    def show_installation_history(self):

        self.clear_page()

        self.create_page_title(
            "Installation History",
            "View previous installation attempts recorded in the database"
        )

        history = get_installation_history()

        summary_label = tk.Label(
            self.main_area,
            text=f"TOTAL RECORDS: {len(history)}",
            bg="#101827",
            fg="#38bdf8",
            font=("Arial", 12, "bold")
        )

        summary_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 15)
        )

        columns = (
            "id",
            "tool",
            "status",
            "timestamp",
            "message"
        )

        table = ttk.Treeview(
            self.main_area,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "tool": "TOOL",
            "status": "RESULT",
            "timestamp": "DATE AND TIME",
            "message": "MESSAGE"
        }

        widths = {
            "id": 50,
            "tool": 110,
            "status": 130,
            "timestamp": 190,
            "message": 350
        }

        for column in columns:

            table.heading(
                column,
                text=headings[column]
            )

            table.column(
                column,
                width=widths[column],
                anchor="w"
            )

        table.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        def refresh_history():

            for item in table.get_children():
                table.delete(item)

            records = get_installation_history()

            for record in records:

                table.insert(
                    "",
                    "end",
                    values=(
                        record.get("id", ""),
                        record.get("tool_name", ""),
                        record.get("status", ""),
                        record.get("timestamp", ""),
                        record.get("message", "")
                    )
                )

            summary_label.config(
                text=f"TOTAL RECORDS: {len(records)}"
            )

        tk.Button(
            self.main_area,
            text="Refresh History",
            command=refresh_history,
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=18,
            pady=10
        ).pack(anchor="e", padx=30, pady=15)

        refresh_history()

    # --------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------

    def show_error(self, error):

        messagebox.showerror(
            "Error",
            str(error)
        )


# --------------------------------------------------
# APPLICATION ENTRY POINT
# --------------------------------------------------

def run_app():

    root = tk.Tk()

    GuardianApp(root)

    root.mainloop()
