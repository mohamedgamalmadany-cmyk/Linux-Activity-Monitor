#!/usr/bin/env python3
"""
Activity Monitor - Start Here
Main entry point
"""

import tkinter as tk
import database.database_operations as db
from gui.dashboard_main import Dashboard


def main():
    """Main function"""
    # Create database
    db.create_database()
    
    # Start GUI
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
